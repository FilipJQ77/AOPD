#!/bin/bash

# <plik> <typ: 1 - naive, 2 - accelerated, <start_point>, <stop_point>, <samples>, <function 1-6>, <repetitions>, <show plot>
samples=100000000
function=1
repetitions=1
show_plot=0
repetitions_bash=10
start_point=1
stop_point=10
filename="results100mil.csv"
for function in {1,2,3,4,5,6};do
    for implementation in {1,2};do
        for ((i = 0 ; i < "$repetitions_bash" ; i++));do
            echo "$implementation $start_point $stop_point $samples $function $repetitions $show_plot"
            python "./main.py" "$implementation" "$start_point" "$stop_point" "$samples" "$function" "$repetitions" "$show_plot" "$filename"
        done
    done
done
