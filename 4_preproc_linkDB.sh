#/bin/bash
if [ $# -lt 1 ]
then
  echo "Directory name needed"
  exit
fi

DIR_N=$1

echo "#######################################"
echo "#   Pre-processing part #4            #"
echo "#     Link and move DB directory      #"
echo "#######################################"

DB_DIR="$DIR_N/DB"
mkdir $DB_DIR

rm -f $DB_DIR/dhs
rm -f $DB_DIR/histone
rm -f $DB_DIR/pathway

ln -s $PWD/CommonDB/dhs     $DB_DIR/dhs
ln -s $PWD/CommonDB/histone $DB_DIR/histone
ln -s $PWD/CommonDB/pathway $DB_DIR/pathway
mv        PreProc/fimo/DB   $DB_DIR/fimo

cd $DB_DIR
rm -f num_classes.tsv
for D in dhs histone pathway fimo
do
  wc -l $D/class_name.tsv >> num_class.txt
done

