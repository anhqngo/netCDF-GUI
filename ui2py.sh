#!/bin/bash

# This bash script converts all designer files (.ui) to python files (.py)
for file in ./src/main/resources/designer/*;
do
    temp=${file##*/}
    pyuic5 ${file} -o ./src/main/python/ui/${temp%.*}.py
done