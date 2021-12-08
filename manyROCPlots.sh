#!/bin/bash

declare -a objArray=("Higgs")
declare -a regionArray=("ehad" "emu" "hadhad" "muhad" "tot")
declare -a bkgArray=("dyll" "diboson" "wjets" "qcd" "bkg")
declare -a sigArray=("ggHHto2b2tau")
declare -a epochArray=("epoch10")
declare -a bkgValArray=("dyll" "diboson" "wjets" "qcd" "bkg")
declare -a sigValArray=("ggHHto2b2tau" "vbfHto2tau" "ggHto2tau")

dir=$1
saveDir=$2

# Iterate the string array using for loop
for obj in ${objArray[@]}; do
    for region in ${regionArray[@]}; do
        totfiles=""
        totmodels=""
        totlabels=""
        for sig in ${sigArray[@]}; do
            for bkg in ${bkgArray[@]}; do
                files=""
                models=""
                labels=""
                #for bkgVal in ${bkgValArray[@]}; do
                #    for sigVal in ${sigValArray[@]}; do
                #            totfiles+="${dir}/di${obj}_Train${sig}_bkg_Val${sigVal}_${bkgVal}_${region}_epoch10/test_ROC_data.pickle;"
                #            totmodels+="${dir}/di${obj}_Train${sig}_bkg_Val${sigVal}_${bkgVal}_${region}_epoch10/model_INFO.txt;"
                #            totlabels+="${sig}_epoch10;"
                #    done
                #done

                for bkgVal in ${bkgValArray[@]}; do
                    for sigVal in ${sigValArray[@]}; do
                        files+="${dir}/di${obj}_Train${sig}_${bkg}_Val${sigVal}_${bkgVal}_${region}_epoch10/test_ROC_data.pickle;"
                        models+="${dir}/di${obj}_Train${sig}_${bkg}_Val${sigVal}_${bkgVal}_${region}_epoch10/model_INFO.txt;"
                        labels+="Train${sig}_${bkg}_Val${sigVal}_${bkgVal}_${region}_epoch10;"
                    done
                done
                echo ${sig} vs. ${bkg}
                echo python rocPlot.py -n ${obj}_${sig}_${region} -d ${dir}/${saveDir} -f "${files}" -m "${models}" -l "${labels}"
                python rocPlot.py -n ${obj}_Train${sig}_${bkg}_${region} -d ${dir}/${saveDir} -f "${files}" -m "${models}" -l "${labels}"
            done        
        done
    
        echo python rocPlot.py -n ${obj}_totBkg_${region} -d ${dir}/${saveDir} -f "${totfiles}" -m "${totmodels}" -l "${totlabels}"
        python rocPlot.py -n ${obj}_totBkg_${region} -d ${dir}/${saveDir} -f "${totfiles}" -m "${totmodels}" -l "${totlabels}"
    
    done
done
