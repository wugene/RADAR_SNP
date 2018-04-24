#!/bin/bash
cd download

rm -f merge_*
cat ../01_file_list.tsv \
| awk -F"\/" '{print $NF}' \
| awk '{print "zcat", $1, "| awk -f ../11_print_class.awk -v CL=" $2}' \
| sh 

rm -f merge_chrX.bed merge_chrY.bed merge_chrM.bed merge_chr*_*.bed
cd ..


rm -rf DB
mkdir DB

cut -f4 download/merge_chr*.bed \
| uniq | sort -u \
| awk '{print NR-1 "\t" $1}' \
> DB/class_name.tsv
