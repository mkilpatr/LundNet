#!/bin/bash

declare -a regionArray=("ehad" "emu" "hadhad" "muhad")
declare -a bkgArray=("dyll" "diboson" "wjets" "bkg")
declare -a sigArray=("ggHHto2b2tau" "vbfHto2tau" "ggHto2tau")

dir=$1

# Iterate the string array using for loop
for sig in ${sigArray[@]}; do
    for bkg in ${bkgArray[@]}; do
        for region in ${regionArray[@]}; do
        
            echo lundnet --model lundnet5 --dir ${dir}_${region} --sig genHiggs_${sig}.json.gz --bkg genHiggs_${bkg}.json.gz --save diHiggs_${sig}_${bkg}_${region} --device cpu --num-epochs 1
            lundnet --model lundnet5 --dir ${dir}_${region} --sig genHiggs_${sig}.json.gz --bkg genHiggs_${bkg}.json.gz --save diHiggs_${sig}_${bkg}_${region} --device cpu --num-epochs 1
        
        done
    done
done
