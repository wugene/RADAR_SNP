#/bin/bash
mkdir download
cd download

if [ $# -lt 1 ]
then
  echo "Need filename"
  exit
fi

SNP_FILE="../$1"

FTP_SITE=ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502
FILE1="$FTP_SITE/ALL."
FILE2=".phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz"

for i in `seq 1 22`
do
  echo "wget -nc $FILE1""chr$i$FILE2.tbi" \
  | tee /dev/stderr
done | parallel -j 22

cat $SNP_FILE \
| awk -v F1="$FILE1" -v F2="$FILE2" '
  {
    min = $2-200000;
    if (min < 0) min=0;
    max = $2+200000;
    print "tabix", F1 $1 F2, substr($1,4) ":" min "-" max, ">", "1kg." $4 ".vcf";
  }
' \
| tee /dev/stderr \
| parallel -j 20

