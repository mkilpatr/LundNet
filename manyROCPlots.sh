#!/bin/bash

declare -a regionArray=("ehad" "emu" "hadhad" "muhad")
declare -a bkgArray=("dyll" "diboson" "wjets" "bkg")
declare -a sigArray=("ggHHto2b2tau" "vbfHto2tau" "ggHto2tau")

dir=$1

# Iterate the string array using for loop
for region in ${regionArray[@]}; do
    for sig in ${sigArray[@]}; do
        
        echo python rocPlot.py -n ${sig}_${region} -d ${dir}/ROCPlots -f "${dir}/diHiggs_${sig}_dyll_${region}/test_ROC_data.pickle;${dir}/diHiggs_${sig}_diboson_${region}/test_ROC_data.pickle;${dir}/diHiggs_${sig}_wjets_${region}/test_ROC_data.pickle" -m "${dir}/diHiggs_${sig}_dyll_${region}/model_INFO.txt;${dir}/diHiggs_${sig}_diboson_${region}/model_INFO.txt;${dir}/diHiggs_${sig}_wjets_${region}/model_INFO.txt" -l "Dyll;Diboson;W+jets"
        python rocPlot.py -n ${sig}_${region} -d ${dir}/ROCPlots -f "${dir}/diHiggs_${sig}_dyll_${region}/test_ROC_data.pickle;${dir}/diHiggs_${sig}_diboson_${region}/test_ROC_data.pickle;${dir}/diHiggs_${sig}_wjets_${region}/test_ROC_data.pickle" -m "${dir}/diHiggs_${sig}_dyll_${region}/model_INFO.txt;${dir}/diHiggs_${sig}_diboson_${region}/model_INFO.txt;${dir}/diHiggs_${sig}_wjets_${region}/model_INFO.txt" -l "Dyll;Diboson;W+jets"

    done

    python rocPlot.py -n totBkg_${region} -d ${dir}/ROCPlots -f "${dir}/diHiggs_ggHHto2b2tau_bkg_${region}/test_ROC_data.pickle;${dir}/diHiggs_vbfHto2tau_bkg_${region}/test_ROC_data.pickle;${dir}/diHiggs_ggHto2tau_bkg_${region}/test_ROC_data.pickle" -m "${dir}/diHiggs_ggHHto2b2tau_bkg_${region}/model_INFO.txt;${dir}/diHiggs_vbfHto2tau_bkg_${region}/model_INFO.txt;${dir}/diHiggs_ggHto2tau_bkg_${region}/model_INFO.txt" -l "ggToHH;vbfH;ggH"

done
