
NR==FNR{
  CN[$2]=$1; 
  next;
} 
$4 in CN{ 
  printf "%04x%08x%08x", CN[$4], $2, $3 > "merged_" $1 ".hex";
}
