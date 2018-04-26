#/bin/bash
if [ $# -lt 1 ]
then
  echo "No argument"
  exit
fi

FN=$1

for i in 1
do
  cat $FN \
  | awk -F"\t" '
    $12>=1 && $12<23{
      OFS="\t";
      split($12,a, ";")
      split($13,b, ";")
      split($22,c, ";")
      print a[1], b[1], c[1], $28}
  '

  cat $FN \
  | awk -F"\t" '
    $12==""{
      OFS="\t"; 
      split(substr($22,4),a,":"); 
      if (a[1]*1 >= 1 && a[1]*1<23) 
        print a[1]*1, a[2], $22, $28;
    }
  ' 
done \
| sort -k4,4g \
| awk '
  {
    #check proximity (200k) to high significant snp
    for (i=1; i<NR; i++) {
      if (($1 == CHR[i]) && ($2 > POS[i]-200000) && ($2 < POS[i]+200000)){
        CHR[NR]=0;
        print "Warning: line", NR, "overlap to line", i, "SKIPPED" > "/dev/stderr";
        next;
      }
    }
    print;
    CHR[NR]=$1;
    POS[NR]=$2;
  }
'
