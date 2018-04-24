#!/bin/bash

MOTIF="download/HOCOMOCOv11_full_HUMAN_mono_meme_format.meme"
for F in `ls SNP/snp*.fa`
do
  echo "fimo -text -parse-genomic-coord -thresh 3e-4 $MOTIF $F > $F.fimo" \
  | tee /dev/stderr
done #| parallel -j 22


cd SNP
for F in `ls snp*.fimo`
do
  echo "awk -f ../21_motif.awk $F" \
  | tee /dev/stderr
done | parallel -j 22
cd ..


rm -rf DB
mkdir DB

cut -f4 SNP/merge*.bed \
| uniq | sort -u \
| awk '
  {
    print NR-1 "\t" $1;
  }' \
> DB/class_name.tsv
