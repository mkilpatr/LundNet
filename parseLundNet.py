import os
import io
import json
import argparse
import re

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

def sortmodel():
    tuples = zip(*sorted(zip(model_auc, model_list)))
    #sorted(model_list, key=lambda x: (model[args.baseDir][x]["train_bkg"], model[args.baseDir][x]["test_bkg"]))
    auc, list = [ list(tuple) for tuple in  tuples]

    res_ = my_dictionary()
    res_.add(args.baseDir, my_dictionary())
    for m in list:
        res_[args.baseDir].add(m, model[args.baseDir][m])
    return res_


for d in Dist:
    if 'diHiggs' not in d: continue
    readModel(d)

models = sortmodel()
json = json.dumps(models, sort_keys=False, indent=2)
f = open(args.baseDir + "/TotalSummary.json", "w")
f.write(json)
f.close()
