#/bin/bash
#if [ $# -lt 1 ]
#then
#  echo "No argument"
#  exit
#fi
#LD_SNP=$1

echo "#######################################"
echo "#   Pre-processing part #2            #"
echo "#     Download pre-processed files    #"
echo "#######################################"
cd CommonDB/

./0_download_DB.sh
echo Download complete in CommonDB/

cd ..


