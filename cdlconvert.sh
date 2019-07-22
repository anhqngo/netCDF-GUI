#!/bin/bash

for file in ./netcdf0/*;
do
    temp=${file##*/}
    ncdump ${file} > ${temp%.*}.cdl
done