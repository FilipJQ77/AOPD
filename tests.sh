#!/bin/bash
# <plik> <typ: 1 - naive, 2 - accelerated, <start_point>, <stop_point>, <samples>, <function 1-6>, <repetitions>, <show plot>
samples=100000
function=1
repetitions=1
show_plot=0
filename="diff_points.csv"

for implementation in {1,2};do
    for point in 10{00000,0000,000,00,0};do
        echo "$implementation -$point $point $samples $function $repetitions $show_plot"
        python "./main.py" $implementation -$point $point $samples $function $repetitions $show_plot $filename
    done
done

start_point=0
stop_point=10
filename="results.csv"


for implementation in {1,2};do
    for function in {1,2,3,4,5,6};do
        for samples in 100{0,00};do
            echo "$implementation $start_point $stop_point $samples $function $repetitions $show_plot"
            python "./main.py" $implementation $start_point $stop_point $samples $function $repetitions $show_plot $filename
        done
    done
done
