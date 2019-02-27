

echo "GWAS catalog file to bed file with hg19"
echo "skip if you already have good snp list for LD extension"
./0_get_snplist.sh BreastCancer/gwas-association-downloaded.tsv.gz
echo "creating gwas-association-downloaded.tsv.hg19.bed"


echo "LD extension with 1000 genome and r-square value"
echo "This takes long time to download 1000 genome data !!"
echo "skip if you already have snp list with LD extended"
./1_preproc_LD_ext.sh gwas-association-downloaded.tsv.hg19.bed
echo "creating BreastCancer/All_LD_snp.bed"


echo "Download pre-processed files"
echo "bed files from ENCODE project are preprocessed"
./2_preproc_commonDB.sh
echo "creating dhs, histone, pathway in CommonDB"

echo "CommonDB for fimo is too large"
./3_preproc_fimo.sh BreastCancer
echo "Creating snp specific DB for fimo in PreProc"

echo "DB files are linked to the DIRECTORY"
./4_preproc_linkDB.sh BreastCancer

echo "Run CNN"
echo "All_LD_snp.bed and DB directory should be in the DIRECTORY"
./5_run_cnn.sh BreastCancer
echo "Creating Prediction_result/ in the DIRECTORY"


echo "All_LD_snp.bed is already in RA"
./2_preproc_commonDB.sh
./3_preproc_fimo.sh   RA
./4_preproc_linkDB.sh RA
./5_run_cnn.sh        RA

