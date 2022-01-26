#!/usr/bin/env python
import os
import sys
import argparse

parser = argparse.ArgumentParser(description='Process config file')
parser.add_argument("-s", "--submit", dest="submit", default="submitall", help="Name of shell script to run for job submission. [Default: submitall]")
parser.add_argument("-b", "--basedir", dest="basedir", default="/home/mkilpatr/LundNet", help="Path to base directory. [Default: \"/home/mkilpatr/LundNet\"]")
parser.add_argument("-p", "--pathtodata", dest="path", default=".", help="Path to directory with run macro and configuration file. [Default: \"../\"]")
parser.add_argument("-o", "--outdir", dest="outdir", default="${PWD}/models", help="Output directory for model results, [Default: \"${PWD}/models\"]")
parser.add_argument("-e", "--epochs", dest="epochs", default="10", help="Number of epochs for the training, [Default: \"5\"]")
parser.add_argument("-m", "--model", dest="model", default="lundnet5", help="Model used to train, [Default: \"lundnet5\"]")
parser.add_argument("-u", "--test", dest="test", default=False, help="Do you want to specify the testing files?, [Default: \"False\"]")
parser.add_argument("-t", "--submittype", dest="submittype", default="condor", choices=["interactive","lsf","condor"], help="Method of job submission. [Options: interactive, lsf, condor. Default: condor]")
parser.add_argument("--jobdir", dest="jobdir", default="jobs", help="Job dir. [Default: %(default)s]")
args = parser.parse_args()

regionArray=["ehad", "emu", "hadhad", "muhad", "tot"]
bkgArray=["dyll", "diboson", "wjets", "qcd", "bkg"]
sigArray=["ggHHto2b2tau", "vbfHto2tau", "ggHto2tau"]
objArray=["Higgs"]

bkgValArray = ["dyll", "diboson", "wjets", "qcd", "bkg"] 
sigValArray = ["ggHHto2b2tau", "vbfHto2tau", "ggHto2tau"]

os.system("mkdir -p %s" % args.jobdir)

print("Creating submission file: ",args.submit+".sh")
script = open(args.submit+".sh","w")
script.write("""#!/bin/bash 

outputdir={outdir}
inputdir={pathtodata}
 
""".format(outdir=args.outdir, pathtodata=args.path))

epochStr = "epoch" + str(args.epochs)

for o in objArray:
    for s in sigArray:
        for b in bkgArray:
            for sv in sigValArray:
                for bv in bkgValArray:
                    for reg in regionArray:
                        if args.submittype == "interactive" :
                            script.write("""lundnet --model {model} --dir {dir}/{region} --train-sig gen{obj}_{sigtrain}.json.gz --train-bkg gen{obj}_{bkgtrain}.json.gz --val-sig gen{obj}_{sigval}.json.gz --val-bkg gen{obj}_{bkgval}.json.gz --save {basedir}/{outdir}/di{obj}_Train{sigtrain}_{bkgtrain}_Val{sigval}_{bkgval}_{region}_{epochStr} --device cpu --num-epochs {epochs}\n""".format(
                            dir=args.path, model=args.model, region=reg, sigtrain=s, bkgtrain=b, sigval=sv, bkgval=bv, outdir=args.outdir, epochStr=epochStr, epochs=args.epochs, basedir=args.basedir, obj=o
                            ))
                        elif args.submittype == "condor" :
                            os.system("mkdir -p %s/logs" % args.outdir)
                            jobscript = open(os.path.join(args.jobdir,"submit_{}_{}_{}_{}_{}_{}_{}_{}.job".format(args.model, o, s, b, sv, bv, reg, epochStr)),"w")
                            outputname = ''
                            jobscript.write("""#!/bin/bash
    
#SBATCH -N 1 --partition=gpu --ntasks-per-node=1
#SBATCH --gres=gpu:1

cd $SLURM_SUBMIT_DIR

/bin/hostname
srun --gres=gpu:1 lundnet --model {model} --dir {dir}/{region} --train-sig gen{obj}_{sigtrain}.json.gz --train-bkg gen{obj}_{bkgtrain}.json.gz --val-sig gen{obj}_{sigval}.json.gz --val-bkg gen{obj}_{bkgval}.json.gz --save {basedir}/{outdir}/di{obj}_Train{sigtrain}_{bkgtrain}_Val{sigval}_{bkgval}_{region}_{epochStr} --device cpu --num-epochs {epochs}
""".format(
                            dir=args.path, model=args.model, region=reg, sigtrain=s, bkgtrain=b, sigval=sv, bkgval=bv, outdir=args.outdir, epochStr=epochStr, epochs=args.epochs, basedir=args.basedir, obj=o
                            ))
                            jobscript.close()
                            script.write("sbatch {jobdir}/submit_{model}_{obj}_{sigtrain}_{bkgtrain}_{sigval}_{bkgval}_{region}_{epoch}.job\n".format(jobdir=args.jobdir, model=args.model, obj=o, sigtrain=s, bkgtrain=b, sigval=sv, bkgval=bv, region=reg, epoch=epochStr))
                            os.system("chmod +x %s/submit_%s_%s_%s_%s_%s_%s_%s_%s.job" %(args.jobdir, args.model, o, s, b, sv, bv, reg, epochStr))
        
       
    
script.close()
os.system("chmod +x %s.sh" % args.submit)

print("Done!")
