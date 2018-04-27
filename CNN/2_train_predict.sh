#!/bin/bash
NUM_OF_GPU=8
NUM_OF_ITERATION=12
#NUM_OF_GPU * NUM_OF_ITERATION should be multiple of 6 

MAX_ID_GPU=$(($NUM_OF_GPU-1))
MAX_ITERATION=$(($NUM_OF_ITERATION-1))

rm -rf PRED
mkdir PRED

for i in `seq 0 $MAX_ITERATION`
do
  for j in `seq 0 $MAX_ID_GPU`
  do
    seq_no=$(($i*8+$j))
    echo CUDA_VISIBLE_DEVICES=$j python 22_training_keras.py $seq_no 1>&2
    echo CUDA_VISIBLE_DEVICES=$j python 22_training_keras.py $seq_no
  done | parallel -j 8
done


cat PRED/predict.* \
| sort -V \
| awk '
  {
    key=$1 "\t" $2;
    sum[key]+=int($3+0.5);
    count[key]++;
  }
  END{
    for (k in sum) {
      print k "\t" sum[k]/count[k];
    }
  }' \
| sort -V \
> PRED/all_predict_average.tsv
