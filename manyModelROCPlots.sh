#!/bin/bash

declare -a objArray=("Higgs")
declare -a regionArray=("ehad" "emu" "hadhad" "muhad" "tot")
declare -a bkgArray=("dyll" "diboson" "wjets" "qcd" "bkg")
declare -a sigArray=("ggHHto2b2tau")
declare -a epochArray=("epoch10")
declare -a bkgValArray=("dyll" "diboson" "wjets" "qcd" "bkg")
declare -a sigValArray=("ggHHto2b2tau" "vbfHto2tau" "ggHto2tau")
declare -a modelArray=("lundnet5" "lundnet4" "lundnet3" "lundnet2" "particlenet")

dir=$1
saveDir=$2

# Iterate the string array using for loop
for obj in ${objArray[@]}; do
    for region in ${regionArray[@]}; do
        for sig in ${sigArray[@]}; do
            for bkg in ${bkgArray[@]}; do
                for bkgVal in ${bkgValArray[@]}; do
                    for sigVal in ${sigValArray[@]}; do
                        files=""
                        models=""
                        labels=""
                        for model in ${modelArray[@]}; do
                            files+="${dir}_${model}/di${obj}_Train${sig}_${bkg}_Val${sigVal}_${bkgVal}_${region}_epoch10/test_ROC_data.pickle;"
                            models+="${dir}_${model}/di${obj}_Train${sig}_${bkg}_Val${sigVal}_${bkgVal}_${region}_epoch10/model_INFO.txt;"
                            labels+="${model};"
                        done
                        echo ${sig} vs. ${bkg}
                        echo python rocPlot.py -n ${obj}_${sig}_${region} -d ${dir}/${saveDir} -f "${files}" -m "${models}" -l "${labels}"
                        python rocPlot.py -n ${obj}_Train${sig}_${bkg}_Val${sigVal}_${bkgVal}_${region} -d ${saveDir} -f "${files}" -m "${models}" -l "${labels}"
                    done
                done
            done        
        done
    done
done
