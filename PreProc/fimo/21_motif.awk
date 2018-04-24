
BEGIN{OFS="\t"}
$1=="#"{next;}
{
  split($1,a,"_");
  print $2, $3, $4, a[1] > "merge_" $2 ".bed";
}
