#/bin/bash
if [ $# -lt 1 ]
then
  echo "No argument !"
  echo "argument 1 should be tsv file from GWAS catalog site"

  exit
fi


FN=$1
if [ ${FN: -3} == ".gz" ]
then
    gunzip $FN
fi
FN=${FN%.gz}

cd GWAS_Catalog
FN_IN="../$FN"
F_TSV="../$FN.tsv"
F_HG19="../$FN.hg19.bed"


./11_gwas_tsv_to_bed.sh    $FN_IN > $F_TSV
python ./12_hg38_2_hg19.py $F_TSV > $F_HG19
