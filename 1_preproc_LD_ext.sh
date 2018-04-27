#/bin/bash
if [ $# -lt 1 ]
then
  echo "No argument"
  exit
fi

LD_SNP=$(dirname "$1")/"All_LD_snp.bed"

echo "#######################################"
echo "#   Pre-processing part #1            #"
echo "#     LD extension for SNP            #"
echo "#######################################"
cd PreProc/snp_ld_ext/
FN_IN="../../$1"
F_OUT="../../$LD_SNP"

./0_download.sh $FN_IN
./1_ld_ext_multi.sh $FN_IN > $F_OUT

cd ../..
echo End
echo Outfile= $LD_SNP


