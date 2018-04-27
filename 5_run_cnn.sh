#/bin/bash
if [ $# -lt 1 ]
then
  echo "Directory name needed"
  exit
fi

DIR_N=$1
LD_SNP=$DIR_N/All_LD_snp.bed

echo "#######################################"
echo "#   CNN learning part 1               #"
echo "#      Link DB file to CNN            #"
echo "#######################################"

DB_DIR="$DIR_N/DB"

cd CNN
rm -f DB
ln -s ../$DB_DIR .

#./1_make_pkl.sh ../$LD_SNP
./2_train_predict.sh
