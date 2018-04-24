
# coding: utf-8

# In[1]:


from pandas import DataFrame
import numpy as np
import gzip
import _pickle as pkl


# In[2]:


import sys


# In[3]:

if len(sys.argv)<4:
    print('Need 3 argument')
    print('example: arg[1]="SNP/snp_chr1.bed"')
    print('         arg[2]="DB/dhs/merged_chr1.hex.bin"')
    print('         arg[3]="PKL/dhs_chr1.pkl.gz"')
    exit()
else:
    snp_f, bin_f, pkl_f = sys.argv[1:4]



print("Input SNP: %s\tDB: %s" % (snp_f,bin_f))

# In[ ]:

pos_l = list()
merge_l = list()

# Process SNP
with open(snp_f) as f:
    for line in f:
        pos = int(line.split("\t")[1])
        pos_l.append( pos+0.5 )
        merge_l.append( [0,0] )

# Process DB BIN
max_cl = 0
with open(bin_f, 'rb') as f:
    while True:
        s  = f.read(2)
        cl =   int.from_bytes(s, byteorder='big')
        if (max_cl < cl):
            max_cl = cl
        s  = f.read(4)
        pos1 = int.from_bytes(s, byteorder='big')
        s  = f.read(4)
        pos2 = int.from_bytes(s, byteorder='big')
        if (pos2 == 0):
            break

        pos_l.append(pos1)
        merge_l.append([cl,  1])

        pos_l.append(pos2)
        merge_l.append([cl, -1])

# position to sort
pos_np = np.array(pos_l)
sorted_id = pos_np.argsort()


# multiple intersection
flags = [0] * (max_cl + 1)
res_d = dict()

for iid in sorted_id:
    line = merge_l[iid]
    switch = line[1]
    if switch==0:
        pos = int(pos_l[iid])
        res_d[pos] = np.nonzero(flags)
    else:
        cl = line[0]
        flags[ cl ] += switch

# dump result
print("Output PKL: %s" % (pkl_f))
pkl.dump(res_d, gzip.open(pkl_f, 'wb'))

