

drwxr-xr-x  2 wooyang user  4096 Apr 27 15:52 BreastCancer/
drwxr-xr-x  5 wooyang user  4096 Apr 27 13:41 CNN/
drwxr-xr-x  5 wooyang user  4096 Apr 27 12:54 CommonDB/
-rw-r--r--  1 wooyang user  1654 Apr 27 12:45 favicon.png
drwxr-xr-x  8 wooyang user  4096 Apr 27 15:49 .git/
-rw-r--r--  1 wooyang user   328 Apr 27 15:48 .gitignore
drwxr-xr-x  2 wooyang user  4096 Apr 27 15:46 GWAS_Catalog/
drwxr-xr-x  6 wooyang user  4096 Apr 27 12:45 PreProc/
drwxr-xr-x  4 wooyang user  4096 Apr 27 13:41 RA/
-rw-r--r--  1 wooyang user 17851 Apr 27 12:45 radar_snp_banner.jpg
-rw-r--r--  1 wooyang user    82 Apr 27 12:45 README.md
-rwxr-xr-x  1 wooyang user     0 Apr 27 15:51 run_example.sh*
drwxr-xr-x  2 wooyang user  4096 Apr 27 12:45 testing/
wooyang@omicsGPU:~/jupyter/RADAR_SNP$
wooyang@omicsGPU:~/jupyter/RADAR_SNP$
wooyang@omicsGPU:~/jupyter/RADAR_SNP$ more BreastCancer/
All_LD_snp.bed                            gwas-association-downloaded.tsv.hg19.bed  README
gwas-association-downloaded.tsv           gwas-association-downloaded.tsv.tsv
wooyang@omicsGPU:~/jupyter/RADAR_SNP$ ll BreastCancer/
total 1540
drwxr-xr-x  2 wooyang user   4096 Apr 27 15:52 ./
drwxr-xr-x 10 wooyang user   4096 Apr 27 15:51 ../
-rw-r--r--  1 wooyang user 596142 Apr 27 12:45 All_LD_snp.bed
-rw-r--r--  1 wooyang user 910428 Apr 27 12:45 gwas-association-downloaded.tsv
-rw-r--r--  1 wooyang user  27204 Apr 27 15:52 gwas-association-downloaded.tsv.hg19.bed
-rw-r--r--  1 wooyang user  21819 Apr 27 15:52 gwas-association-downloaded.tsv.tsv
-rw-r--r--  1 wooyang user    162 Apr 27 12:45 README

echo "GWAS catalog file to bed file with hg19"
echo "skip if you already have good snp list for LD extension"
./0_get_snplist.sh BreastCancer/gwas-association-downloaded.tsv.gz
echo "creating gwas-association-downloaded.tsv.hg19.bed"


echo "LD extension with 1000 genome and r-square value"
echo "This takes long time to download 1000 genome data !!"
echo "skip if you already have snp list with LD extended"
./1_preproc_LD_ext.sh gwas-association-downloaded.tsv.hg19.bed
echo "creating All_LD_snp.bed"


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

