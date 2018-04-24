#!/bin/bash
if [ $# -lt 1 ]
then
  echo "No argument ! use example file to process"
  FN="../../example/all_ld_snps.bed"
else
  FN=$1
fi

rm -rf SNP
mkdir SNP


cat $FN \
| awk '
  {
    print $1 "\t" $2-100 "\t" $3+100;
  }' \
| sort -u > SNP/snp_list.bed

cd SNP

for F in `ls ../download/chr*.fa`
do
  SNP_F=snp_list.$(basename -- "$F")
  echo bedtools getfasta -fi $F -bed snp_list.bed -fo snp_list.$SNP_F \
  | tee /dev/stderr
done | parallel -j 40





