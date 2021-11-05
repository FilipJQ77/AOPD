#!/bin/bash

# <plik> <typ: 1 - naive, 2 - accelerated, <start_point>, <stop_point>, <samples>, <function 1-6>, <repetitions>, <show plot>
samples=1000000
function=1
repetitions=1
show_plot=0

filename="diff_points.csv"
for implementation in {1,2};do
    for point in {1000000,100000,10000,1000,100,10,1,0.1,0.01,0.001};do
        echo "$implementation -$point $point $samples $function $repetitions $show_plot"
        python "./main.py" "$implementation" -"$point" "$point" "$samples" "$function" "$repetitions" "$show_plot" "$filename"
    done
done

start_point=1
stop_point=10
filename="results.csv"
for function in {1,2,3,4,5,6};do
    for implementation in {2,1};do
        for samples in {1000,10000,100000,1000000,10000000,100000000};do
            echo "$implementation $start_point $stop_point $samples $function $repetitions $show_plot"
            python "./main.py" "$implementation" "$start_point" "$stop_point" "$samples" "$function" "$repetitions" "$show_plot" "$filename"
        done
    done
done
