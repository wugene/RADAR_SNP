{
  OFS="\t";
  print $1, $2, $3, CL >> "merge_" $1 ".bed";
}
