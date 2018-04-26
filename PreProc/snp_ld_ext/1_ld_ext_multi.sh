#!/bin/bash



if [ $# -lt 1 ]
then
  echo "No argument"
  exit
fi

FN=$1


NUM_GPU=`nvidia-smi -L | wc -l`
NUM_JOB=$NUM_GPU
if [ $NUM_JOB -lt 1 ]
then
  $NUM_JOB=`cat /proc/cpuinfo | grep "^processor" | wc -l`


echo -e "#chr\tpos1\tpos2\tgwas_snp"


cat $FN \
| awk -v N_GPU=$NUM_GPU '
  {
    if (N_GPU>0){
      printf "CUDA_VISIBLE_DEVICES=" NR%N_GPU
    }
    print " python 11_ld_ext_by_r_sq.py", $4, $2;
  }
' | tee /dev/stderr \
| parallel -j $((NUM_JOB * 1)) 

