#!/bin/bash

#
pol="423"
for file in $(ls -1 *.nc);do
	python program.py -v tg,rr $file
        mv output/output.csv output/output_${pol}_${file}.csv
done

