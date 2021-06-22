#!/usr/bin/env python
import os
import sys
import argparse

parser = argparse.ArgumentParser(description='Process config file')
parser.add_argument("-s", "--submit", dest="submit", default="submitall", help="Name of shell script to run for job submission. [Default: submitall]")
parser.add_argument("-b", "--basedir", dest="basedir", default="/home/mkilpatr/LundNet", help="Path to base directory. [Default: \"/home/mkilpatr/LundNet\"]")
parser.add_argument("-p", "--pathtodata", dest="path", default=".", help="Path to directory with run macro and configuration file. [Default: \"../\"]")
parser.add_argument("-o", "--outdir", dest="outdir", default="${PWD}/models", help="Output directory for model results, [Default: \"${PWD}/models\"]")
parser.add_argument("-e", "--epochs", dest="epochs", default="5", help="Number of epochs for the training, [Default: \"5\"]")
parser.add_argument("-t", "--submittype", dest="submittype", default="condor", choices=["interactive","lsf","condor"], help="Method of job submission. [Options: interactive, lsf, condor. Default: condor]")
parser.add_argument("--jobdir", dest="jobdir", default="jobs", help="Job dir. [Default: %(default)s]")
args = parser.parse_args()

regionArray=["ehad", "emu", "hadhad", "muhad", "tot"]
bkgArray=["dyll", "diboson", "wjets", "bkg"]
sigArray=["ggHHto2b2tau", "vbfHto2tau", "ggHto2tau"]

os.system("mkdir -p %s" % args.jobdir)

print("Creating submission file: ",args.submit+".sh")
script = open(args.submit+".sh","w")
script.write("""#!/bin/bash 

outputdir={outdir}
inputdir={pathtodata}
 
""".format(outdir=args.outdir, pathtodata=args.path))

epochStr = "epoch" + str(args.epochs)

for s in sigArray:
    for b in bkgArray:
        for reg in regionArray:
            if args.submittype == "interactive" :
                script.write("""lundnet --model lundnet5 --dir {dir}_{region} --sig genHiggs_{sig}.json.gz --bkg genHiggs_{bkg}.json.gz --save {basedir}/{outdir}/diHiggs_{sig}_{bkg}_{region}_{epochStr} --device cpu --num-epochs {epochs}\n""".format(
                dir=args.path, region=reg, sig=s, bkg=b, outdir=args.outdir, epochStr=epochStr, epochs=args.epochs, basedir=args.basedir
                ))
            elif args.submittype == "condor" :
                os.system("mkdir -p %s/logs" % args.outdir)
                jobscript = open(os.path.join(args.jobdir,"submit_{}_{}_{}.job".format(s, b, reg)),"w")
                outputname = ''
                jobscript.write("""#!/bin/bash

#SBATCH -N 1 --partition=gpu --ntasks-per-node=1
#SBATCH --gres=gpu:1

export MODEL_NAME=v12_lazy_3region_extended

cd $SLURM_SUBMIT_DIR

/bin/hostname
srun --gres=gpu:1 lundnet --model lundnet5 --dir {dir}_{region} --sig genHiggs_{sig}.json.gz --bkg genHiggs_{bkg}.json.gz --save {basedir}/{outdir}/diHiggs_{sig}_{bkg}_{region}_{epochStr} --device cpu --num-epochs {epochs}
""".format(
            dir=args.path, region=reg, sig=s, bkg=b, outdir=args.outdir, epochStr=epochStr, epochs=args.epochs, basedir=args.basedir
            ))
            jobscript.close()
            script.write("sbatch {jobdir}/submit_{sig}_{bkg}_{region}.job\n".format(jobdir=args.jobdir, sig=s, bkg=b, region=reg))
            os.system("chmod +x %s/submit_%s_%s_%s.job" %(args.jobdir, s, b, reg))
        
       
    
script.close()
os.system("chmod +x %s.sh" % args.submit)

print("Done!")
