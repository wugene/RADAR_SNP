import sys

from pandas import DataFrame
import numpy as np
import gzip
import _pickle as pkl


if len(sys.argv)<2:
    print("No argument ! Use example file")
    snp_f = '../example/all_ld_snps.bed'
else:
    snp_f = sys.argv[1]

# Set input and output

kinds = ['dhs','histone','pathway','fimo']
pkl_f = 'PKL/true_set_merged.pkl.gz'
print("Input SNP: %s\nInput pkl files for %s" % (snp_f, kinds))
print("Output PKL: %s" % (pkl_f))


# Get # of classes

n_cl = dict()
for line in open('DB/num_class.txt'):
    num, kind = line.split(sep='/')[0].split()
    n_cl[kind] = int(num)



# Get all pkls from BED processing

db_dict = dict()
for chrom in range(1,23):
    for kind in kinds:
        k  = ("chr"+str(chrom), kind)
        fn = 'PKL/%s_chr%d.pkl.gz' % (kind, chrom)
        
        db_dict[k] = pkl.load(gzip.open( fn, 'rb'))



# In[33]:

def db_dict_search(chrom, kind, pos):
    pos_id = db_dict[(chrom, kind)][pos]

    pos_dense = np.zeros( n_cl[kind] )
    pos_dense[pos_id] = 1

    return pos_dense

#BUGGY
def db_dict_search_to_bytearray(chrom, kind, pos):
    pos_id = db_dict[(chrom, kind)][pos]

    pos_dense = bytearray(n_cl[kind])
    for i in pos_id:
        pos_dense[i] = 1

    return pos_dense


# In[34]:


snp_df = DataFrame.from_csv(snp_f, sep='\t', index_col=None)
snp_3split_array_label = ( (dict(), dict()), (dict(), dict()), (dict(), dict()) )
snp_split = dict()
for i in range(1,5,1):
    snp_split[ "chr%d" % i ] = 0 # set 1
for i in range(5,10,1):
    snp_split[ "chr%d" % i ] = 1 # set 2
for i in range(10,23,1):
    snp_split[ "chr%d" % i ] = 2 # set 3

for k, v in snp_df.iterrows():
    if v['class'] != 'RA':
        continue
    chrom = v['#chr']
    pos = v['pos1']
    gwas = v['gwas_snp']

    l_kind = list()
    for kind in kinds:
        l_kind.append(db_dict_search(chrom, kind, pos))

    snp_dict, label_dict = snp_3split_array_label[ snp_split[chrom] ]
    if gwas not in snp_dict:
        snp_dict[gwas] = list()
        label_dict[gwas] = list()

    snp_dict[gwas].append( l_kind )
    label_dict[gwas].append( ( chrom, pos ) )


# Save train, valid, test sets

pkl.dump(snp_3split_array_label, gzip.open(pkl_f, 'wb'))
print("Output complete: %s" % (pkl_f))

