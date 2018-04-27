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
    print $1 "\t" $2-100 "\t" $3+100 > "SNP/snp_" $1 ".fa.bed";
  }'

cd SNP

for F in `ls ../download/chr*.fa`
do
  SNP_IN=snp_$(basename "$F").bed
  FA_OUT=snp_list.$(basename "$F")
  echo bedtools getfasta -fi $F -bed $SNP_IN -fo $FA_OUT \
  | tee /dev/stderr
done | parallel -j 40





