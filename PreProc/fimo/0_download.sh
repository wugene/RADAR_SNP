
mkdir download
cd download

URL="http://hocomoco11.autosome.ru/final_bundle/hocomoco11/full/HUMAN/mono/HOCOMOCOv11_full_HUMAN_mono_meme_format.meme"
wget -N $URL


for CHROM in `seq 1 22`
do
  FN="chr$CHROM.fa"
  if [ -f "$FN" ]
  then
    echo "$FN found." > /dev/stderr
    continue
  fi

  URL="http://hgdownload.cse.ucsc.edu/goldenPath/hg19/chromosomes/$FN.gz"
  echo "wget -N $URL"
done | parallel -j 22

gunzip *.fa.gz 
