#!/bin/bash
if [ $# -lt 1 ]
then
  echo "No argument ! use example file to process"
  FN="../example/all_ld_snps.bed"
else
  FN=$1
fi


./10_preproc_snp_list.sh $FN

rm -rf PKL
mkdir PKL

for i in `seq 1 22`
do
  snp_f="SNP/snp_chr$i.bed"
  for j in dhs histone pathway fimo
  do
    bin_f="DB/$j/merged_chr$i.hex.bin"
    pkl_f="PKL/$j""_chr$i.pkl.gz"

    echo "python 11_snp_db_2_pkl.py $snp_f $bin_f $pkl_f" | tee /dev/stderr
  done
done | parallel -j 20


python 12_merge_pkls.py $FN
