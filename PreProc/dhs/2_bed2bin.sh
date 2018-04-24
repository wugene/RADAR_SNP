
cd DB

for B in `ls ../download/merge_*.bed`
do
  echo awk -f ../21_hex.awk class_name.tsv $B \
  | tee /dev/stderr
done | parallel -j 22


for H in `ls *.hex`
do
  echo "xxd -r -p $H > $H.bin" \
  | tee /dev/stderr
done | parallel -j 22

rm -f *.hex
