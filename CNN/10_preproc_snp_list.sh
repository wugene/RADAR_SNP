#!/bin/bash
if [ $# -lt 1 ]
then
  echo "No argument ! use example file to process"
  FN="../example/all_ld_snps.bed"
else
  FN=$1
fi

rm -rf SNP
mkdir SNP

echo "Processing $FN"

awk '
  BEGIN{OFS="\t"}
  $1~"#"{next;}
  {
    print $1, $2, $3 > "SNP/snp_" $1 ".bed";
  }
' $FN 
