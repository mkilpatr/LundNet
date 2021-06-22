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


# make one plot per pt cut with multiple models per plot
def makeCutPlots(plotter):
    p = plotter
    style = "solid"

    # get files
    name = p.name
    files = p.files
    models = p.models
    labels = p.labels
    
    PtCutList = []
    # get p_t cut maps from files
    for file1 in files:
        print("OPENING PICKLE; NAME: {0} FILE: {1}".format(name, file1))
        f1 = open(file1, "rb")
        PtCutMap = pickle.load(f1) 
        PtCutList.append(PtCutMap)

    PtModel = {}
    for model1, label in zip(models, labels):
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
    for file1, label in zip(files, labels):
        PtCutMap = PtCutList[ifile]
        color = p.colors[ifile]
        print("File: {0} Label: {1} Color: {2}".format(file1, label, color))
        TPRPtCut  = PtCutMap["signal_eff"]  
        FPRPtCut  = PtCutMap["background_eff"] 

        plotRocAx.text(0.5, 0.55, name)        
        plotRocAx.text(0.5, 0.5 - 0.05*ifile, label + ": auc = " + str(round(Decimal(PtModel[label]["auc"]), 6)))
        #rocs.append(plotRocAx.plot(FPRPtCut,      TPRPtCut, label=label, linestyle=style, color=color, alpha=1.0)[0])
        rocs.append(plotRocAx.plot(1-FPRPtCut,      TPRPtCut, label=label, linestyle=style, color=color, alpha=1.0)[0])
        ifile += 1
    
    fileLabel = "signal_eff"
    plotLabel = ""
    
    # crate plot for each cut
    first_legend = plotRocAx.legend(handles=rocs, loc="lower right")
    plotRoc.gca().add_artist(first_legend)
    
    plotRocAx.set_xlabel("False Positive Rate")
    plotRocAx.set_ylabel("Signal Efficiency")
    plotRocAx.set_xlim(0.0, 1.0)
    plotRocAx.set_ylim(0.0, 1.0)
    plotRoc.savefig("{0}roc_{1}_{2}.pdf".format(p.outputDirectory, name, fileLabel))
    plt.close(plotRoc)
    
if __name__ == "__main__":
    main()
