import os
import io
import json
import argparse
import re
import math

parser = argparse.ArgumentParser(
        description='Produce or print limits based on existing datacards')
parser.add_argument("-d", "--dir", dest="baseDir", default='.',
                         help="Base directory where files are located")
args = parser.parse_args()

Dist = os.listdir(args.baseDir)

# Create your dictionary class
class my_dictionary(dict):
  
    # __init__ function
    def __init__(self):
        self = dict()
          
    # Function to add key:value
    def add(self, key, value):
        self[key] = value

model = my_dictionary()
model.add(args.baseDir, my_dictionary())
model_list = []
model_auc = []
model_inv_bkg_at_sig_50 = []
model_accuracy = []
auc = []
inv_bkg_at_sig_50 = []
accuracy = []
mlist = []

def readModel(filedir):
    file = open(args.baseDir + "/" + filedir + "/model_INFO.txt", 'r')

    model[args.baseDir].add(filedir, my_dictionary())    
    model_list.append(filedir)
    while True:
        next_line = file.readline()
        if not next_line: break
        if any(x in next_line for x in ["train", "test", "accuracy", "auc", "inv_bkg"]):

            s = next_line.split(": ")
            #print(s)
            substr_ = s[1].strip()
            if re.match(r'^-?\d+(?:\.\d+)$', substr_) is None:
                substr_ = os.path.basename(s[1]).replace(".json.gz", "").strip()
            else:
                substr_ = float(s[1])
            if s[0] == 'auc': model_auc.append(s[1])

            model[args.baseDir][filedir].add(s[0], substr_)

def sortCustom(list1, list2):
    tuples = zip(*sorted(zip(list1, list2), reverse=True))
    list1_, list2_ = [ list(tuple) for tuple in  tuples]
    return list1_, list2_ 

def sortmodel():
    auc, mlist = sortCustom(model_auc, model_list)

    res_ = my_dictionary()
    res_.add(args.baseDir, my_dictionary())
    for m in mlist:
        res_[args.baseDir].add(m, model[args.baseDir][m])
    return res_

def bestValAUC(model, removeQCD = False):
    objArray=["Higgs"]
    regionArray=["ehad", "emu", "hadhad", "muhad", "tot"]
    bkgArray=["dyll", "diboson", "wjets", "qcd", "bkg"]
    sigArray=["ggHHto2b2tau"]
    epochArray=["epoch10"]
    bkgValArray=["dyll", "diboson", "wjets", "qcd", "bkg"]
    sigValArray=["ggHHto2b2tau", "vbfHto2tau", "ggHto2tau"]
    modelArray=["lundnet5", "lundnet4", "lundnet3", "lundnet2", "particlenet"]

    aucRegion = []
    accuracyRegion = []
    effRegion = []
    aucRegionName = []
    # Iterate the string array using for loop
    #diHiggs_TrainggHHto2b2tau_diboson_ValggHto2tau_dyll_hadhad_epoch10
    for obj in objArray:
        for region in regionArray:
            for sig in sigArray:
                for bkg in bkgArray:
                    for sigVal in sigValArray:
                        aucTot = 0.
                        accuracyTot = 0.
                        inv_bkg_at_sig_50Tot = 0.
                        for bkgVal in bkgValArray:
                            if (removeQCD and "qcd" in bkgVal): continue
                            auc = model[args.baseDir]["di" + obj + "_Train" + sig + "_" + bkg + "_Val" + sigVal + "_" + bkgVal + "_" + region + "_epoch10"]["auc"]
                            aucTot += float(auc) if not math.isnan(float(auc)) else 0.
                            accuracy = model[args.baseDir]["di" + obj + "_Train" + sig + "_" + bkg + "_Val" + sigVal + "_" + bkgVal + "_" + region + "_epoch10"]["accuracy"]
                            accuracyTot += float(accuracy) if not math.isnan(float(accuracy)) else 0.
                            inv_bkg_at_sig_50 = model[args.baseDir]["di" + obj + "_Train" + sig + "_" + bkg + "_Val" + sigVal + "_" + bkgVal + "_" + region + "_epoch10"]["inv_bkg_at_sig_50"]
                            inv_bkg_at_sig_50Tot += float(inv_bkg_at_sig_50) if not math.isnan(float(inv_bkg_at_sig_50)) and not math.isinf(float(inv_bkg_at_sig_50)) else 0.
                        aucRegion.append(aucTot)
                        accuracyRegion.append(accuracyTot)
                        effRegion.append(inv_bkg_at_sig_50Tot)
                        aucRegionName.append("di" + obj + "_Train" + sig + "_" + bkg + "_Val" + sigVal + "_" + region)

    accRegionName = aucRegionName
    effRegionName = aucRegionName

    label = " Remove QCD" if removeQCD else ""
    auc, rlist = sortCustom(aucRegion, aucRegionName)
    model[args.baseDir].add("Total AUC" + label, my_dictionary())
    for i, m in enumerate(rlist):
        model[args.baseDir]["Total AUC" + label].add(m, auc[i])

    acc, rlist = sortCustom(accuracyRegion, accRegionName)
    model[args.baseDir].add("Total Accuracy" + label, my_dictionary())
    for i, m in enumerate(rlist):
        model[args.baseDir]["Total Accuracy" + label].add(m, acc[i])

    eff, rlist = sortCustom(effRegion, effRegionName)
    model[args.baseDir].add("Total Eff" + label, my_dictionary())
    for i, m in enumerate(rlist):
        model[args.baseDir]["Total Eff" + label].add(m, eff[i])
    return model

for d in Dist:
    if 'diHiggs' not in d: continue
    readModel(d)

models = sortmodel()
models = bestValAUC(models)
models = bestValAUC(models, True)
json = json.dumps(models, sort_keys=False, indent=2)
f = open(args.baseDir + "/TotalSummary.json", "w")
f.write(json)
f.close()
