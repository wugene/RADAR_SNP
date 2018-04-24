#!/bin/bash
mkdir download
cd download

cat ../01_file_list.tsv \
| awk '{print "wget -nc", $1}' \
| tee /dev/stderr \
| parallel -j 30

cd ..


