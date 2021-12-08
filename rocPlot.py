import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import pickle
import json
import numpy as np
import errno
import os
import optparse
from os.path import exists
from decimal import Decimal
from datetime import datetime

class Plotter:
    def __init__(self):
        self.outputDirectory = ""
        self.jsonFile = "rocPlots.json"
        self.colors = ["red", "blue", "green", "orange", "black", "purple", "yellow", "pink", "maroon", "xkcd:sky blue", "xkcd:violet", "xkcd:cerulean",
                       "xkcd:light red", "xkcd:sea blue", "xkcd:emerald", "xkcd:reddish purple", "xkcd:dark rose", "xkcd:aubergine", "xkcd:teal green", "xkcd:avocado"]


def main():
    parser = optparse.OptionParser("usage: %prog [options]\n")
    parser.add_option('-d', "--directory",   dest='directory',   action='store',      default="",               help="Directory to store outputs")
    parser.add_option('-f', "--files",       dest='files',       action='store',      default="",               help="ROC pkl files, semicolon seperated")
    parser.add_option('-m', "--models",      dest='models',      action='store',      default="",               help="ROC model files, semicolon seperated")
    parser.add_option('-l', "--labels",      dest='labels',      action='store',      default="",               help="Legend labels for each ROC pkl file, semicolon seperated")
    parser.add_option('-n', "--name",        dest='name',        action='store',      default="DAS",            help="String to add to plot name to identify this figure")
    
    options, args = parser.parse_args()

    p = Plotter()
    
    if len(options.directory):
      p.outputDirectory = options.directory
      if p.outputDirectory[-1] != "/":
          p.outputDirectory += "/"
      try:
          os.mkdir(p.outputDirectory)
      except OSError as exc:
          if exc.errno == errno.EEXIST and os.path.isdir(p.outputDirectory):
              pass
          else:
              raise
    
    p.name = options.name
    files = options.files[:-1]
    p.files  = files.split(";")
    if len(options.labels):
        labels = options.labels[:-1]
        p.labels = labels.split(";")
    else:
        p.labels = p.files
    if len(options.models):
        models = options.models[:-1]
        p.models = models.split(";")

    makeCutPlots(p)

sigName = {
    "Higgs" : "Gen Higgs",
    "Taus" : r"Gen $\tau$",
    "ggHHto2b2tau" : r"$ggHH\rightarrow b\bar{b}\tau\tau$",
    "ggHto2tau" : r"$ggH\rightarrow\tau\tau$",
    "vbfHto2tau" : r"$vbfH\rightarrow\tau\tau$",
    "diboson" : "Diboson",
    "dyll" : r"$DY\tau\tau$",
    "wjets" : "W+jets",
    "qcd" : "QCD",
    "tot" : "all regions",
    "bkg" : "Total",
    "totBkg" : "Total",
    "emu" : r"$e\mu$",
    "muhad" : r"$\mu\tau_h$",
    "ehad" : r"$e\tau_h$",
    "hadhad" : r"$\tau_h \tau_h$"
}

# make one plot per pt cut with multiple models per plot
def makeCutPlots(plotter):
    p = plotter
    style = "-"

    # get files
    name = p.name
    files = p.files
    models = p.models
    labels = p.labels
    
    PtCutList = []
    # get p_t cut maps from files
    for file1 in files:
        if not os.path.isfile(file1): continue
        print("OPENING PICKLE; NAME: {0} FILE: {1}".format(name, file1))
        f1 = open(file1, "rb")
        PtCutMap = pickle.load(f1) 
        PtCutList.append(PtCutMap)

    PtModel = {}
    for model1, label in zip(models, labels):
        if not exists(model1): continue
        m1 = open(model1, "r")
        child = {}
        for line in m1:
            lineSplit = line.split(": ")
            child.update({lineSplit[0]: lineSplit[1].rstrip()})
        PtModel.update({label: child})
   
    # plot p_t cuts per file
    plotRoc  = plt.figure()
    plotRocAx  = plotRoc.add_subplot(111)
    rocs  = []
    ifile = 0
    icolor = 0

    newLabels = []
    for file1, label in zip(files, labels):
        if label not in PtModel: continue
        PtCutMap = PtCutList[ifile]
        color = p.colors[icolor]
        print("File: {0} Label: {1} Color: {2}".format(file1, label, color))
        TPRPtCut  = PtCutMap["signal_eff"]  
        FPRPtCut  = PtCutMap["background_eff"] 

        newLabels = label.split("_")
        plotLabel = ""

        if "ValggHto2tau" in file1: 
            style = "-."
        elif "ValvbfHto2tau" in file1: 
            style = "--"
        elif "ValggHHto2b2tau" in file1: 
            style = "-"
        
        plotLabel = sigName[newLabels[2].replace('Val', '')] + " vs. " + sigName[newLabels[3]] + ": auc = " + str(round(Decimal(PtModel[label]["auc"]), 6))
        rocs.append(plotRocAx.plot(1-FPRPtCut,      TPRPtCut, label=plotLabel, linestyle=style, color=color, alpha=1.0)[0])
        if "ValggHto2tau" in file1: icolor += 1
        ifile += 1
    
    fileLabel = "signal_eff"
    plotLabel = name.split("_")

    dyllLine = mlines.Line2D([0], [0], label = 'dyll',color='k', linestyle="-")
    dibosonLine = mlines.Line2D([0], [0], label = 'diboson',color='k', linestyle="--")
    wjets1Line = mlines.Line2D([0], [0], label = 'wjets',color='k', linestyle="-.")
    qcdLine = mlines.Line2D([0], [0], label = 'qcd',color='k', linestyle=":")
    totalLine = mlines.Line2D([0], [0], label = 'Total',color='k', linestyle=(0, (3, 10, 1, 10, 1, 10)))

    #try Log plot
    #plotRocAx.set_yscale('log')    
    #plotRocAx.set_xscale('log')    
    # crate plot for each cut
    first_legend = plotRocAx.legend(handles=rocs.extend([dyllLine, dibosonLine, wjets1Line, qcdLine, totalLine]), loc="lower right", prop={'size': 8})
    plotRoc.gca().add_artist(first_legend)

    plotRocAx.set_title("Gen Higgs Trained on " + sigName[newLabels[0].replace('Train', '')] + " vs. " + sigName[newLabels[1]] + " in " + sigName[newLabels[4]])
    plotRocAx.set_xlabel("False Positive Rate")
    plotRocAx.set_ylabel("Signal Efficiency")
    plotRocAx.set_xlim(0.0, 1.0)
    plotRocAx.set_ylim(0.0, 1.0)
    plotRoc.savefig("{0}roc_{1}_{2}.pdf".format(p.outputDirectory, name, fileLabel))
    plt.close(plotRoc)
    
if __name__ == "__main__":
    main()
