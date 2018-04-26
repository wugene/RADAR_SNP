#/bin/bash
if [ $# -lt 1 ]
then
  echo "No argument"
  exit
fi

FN=$1
FN_OUT=LD_$FN


cd ../PreProc/snp_ld_ext/
./0_download.sh ../../example/$FN
CUDA_VISIBLE_DEVICES=0 python ./1_ld_ext_by_r_sq.py ../../example/$FN > ../../example/$FN_OUT
