
cd DB

for B in `ls ../SNP/merge_*.bed`
do
  echo awk -f ../31_hex.awk class_name.tsv $B \
  | tee /dev/stderr
done | parallel -j 22


for H in `ls *.hex`
do
  echo "xxd -r -p $H > $H.bin" \
  | tee /dev/stderr
done | parallel -j 22

rm -f *.hex
