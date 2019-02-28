#!/bin/bash
DIRS="dhs histone pathway"

for D in $DIRS
do
  mkdir $D
done

cat file_list.tsv \
| awk '{print "wget -N", $1, "-O", $2}' \
| tee /dev/stderr \
| parallel -j 20


