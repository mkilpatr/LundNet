#!/bin/bash

#declare -a regionArray=("ehad" "emu" "hadhad" "muhad" "tot")
declare -a regionArray=("emu")
declare -a bkgArray=("bkg")
declare -a sigArray=("ggHHto2b2tau" "vbfHto2tau" "ggHto2tau")

dir=$1
savedir=$2

# Iterate the string array using for loop
for sig in ${sigArray[@]}; do
    for bkg in ${bkgArray[@]}; do
        for region in ${regionArray[@]}; do
        
            echo lundnet --model lundnet5 --dir ${dir}_${region} --sig genHiggs_${sig}.json.gz --bkg genHiggs_${bkg}.json.gz --save ${savedir}/diHiggs_${sig}_${bkg}_${region}_epoch5 --device cpu --num-epochs 5
            lundnet --model lundnet5 --dir ${dir}_${region} --sig genHiggs_${sig}.json.gz --bkg genHiggs_${bkg}.json.gz --save ${savedir}/diHiggs_${sig}_${bkg}_${region}_epoch5 --device cpu --num-epochs 5
        
        done
    done
done
