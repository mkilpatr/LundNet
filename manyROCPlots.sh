#!/bin/bash

declare -a regionArray=("ehad" "emu" "hadhad" "muhad")
declare -a bkgArray=("dyll" "diboson" "wjets")
declare -a sigArray=("ggHHto2b2tau" "vbfHto2tau" "ggHto2tau")

dir=$1

# Iterate the string array using for loop
for region in ${regionArray[@]}; do
    totfiles=""
    totmodels=""
    totlabels=""
    for sig in ${sigArray[@]}; do
        files=""
        models=""
        labels=""
        totfiles+="${dir}/diHiggs_${sig}_bkg_${region}/test_ROC_data.pickle;"
        totmodels+="${dir}/diHiggs_${sig}_bkg_${region}/model_INFO.txt;"
        totlabels+="${sig};"
        for bkg in ${bkgArray[@]}; do

            files+="${dir}/diHiggs_${sig}_${bkg}_${region}/test_ROC_data.pickle;"
            models+="${dir}/diHiggs_${sig}_${bkg}_${region}/model_INFO.txt;"
            labels+="${bkg};"

        done        


        echo python rocPlot.py -n ${sig}_${region} -d ${dir}/ROCPlots -f "${files}" -m "${models}" -l "${labels}"
        python rocPlot.py -n ${sig}_${region} -d ${dir}/ROCPlots -f "${files}" -m "${models}" -l "${labels}"

    done

    python rocPlot.py -n totBkg_${region} -d ${dir}/ROCPlots -f "${totfiles}" -m "${totmodels}" -l "${totlabels}"

done
