#!/bin/bash
cd DB

DIRS="dhs histone pathway fimo"

for D in $DIRS
do
  mkdir $D
done

cat file_list.tsv \
| awk '{print "wget -nc", $1, "-O", $2}' \
| tee /dev/stderr \
| parallel -j 20


rm -f num_classes.tsv
for D in $DIRS
do
  wc -l $D/class_name.tsv >> num_class.txt
done


