#/bin/bash
if [ $# -lt 1 ]
then
  echo "Directory name needed"
  exit
fi

LD_SNP="$1/All_LD_snp.bed"


echo "#######################################"
echo "#   Pre-processing part #3            #"
echo "#     Download pre-processed files    #"
echo "#######################################"
cd PreProc/fimo/
FN_IN="../../$LD_SNP"

./0_download.sh
./1_get_snp_list.sh $FN_IN
./2_fimo_multi.sh 
./3_bed2bin.sh 

cd ../..

echo DB for FIMO features are created in PreProc/fimo/DB
