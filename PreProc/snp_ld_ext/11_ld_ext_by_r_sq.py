# coding: utf-8

import sys
import numpy as np
#import tensorflow as tf

AF_cutoff=0.005
AF_cutoff_r=1-AF_cutoff


def make_numpy_for_rsqaure(gwas, pos):
    print ("processing %s in pos %s" % (gwas, pos), file=sys.stderr)

    index_l = list()
    numpy_l = list()

    fn = 'download/1kg.%s.vcf' % gwas
    
    with open(fn) as f:
        gwas_arr = list()
        for line in f:
            x = line.strip().split(sep='\t')
            desc_line = x[7]
            vt_chr = desc_line.split(sep=';')[-1]
            if (vt_chr != 'VT=SNP') and (vt_chr !="VT=INDEL"):
                continue

            af_chr = desc_line.split(sep=';')[1]
            AF = float(af_chr.split(sep='=')[1])
            #example 1 217020574 rs7529226 T C 100 PASS AC=191;AF=0.038139;AN=5......

            if ( AF<AF_cutoff ):
                continue

            if ( AF>AF_cutoff_r):
                continue


            snp_arr = np.array([ x.split(sep='|') for x in x[9:] ], dtype=float).flatten()
            index_l.append( (x[0], x[1]) )
            numpy_l.append( snp_arr )

            if (x[2]==gwas):
                gwas_arr = snp_arr
                print("gwas %s is found in chr%s:%s" % (gwas, x[0], x[1]), file=sys.stderr)
            elif ( x[1]==pos ):
                if len(gwas_arr)==0:
                    gwas_arr = snp_arr
                    print("gwas %s is found in chr%s:%s" % (gwas, x[0], x[1]), file=sys.stderr)
    return index_l, numpy_l, gwas_arr



def r_square_top_k(X, y, k):

    X_bar = np.mean(X, axis=1, keepdims=True)
    y_bar = np.mean(y)

    X_2 = X - X_bar
    y_2 = y - y_bar

    X_SS = np.sum((X_2 * X_2), axis=1 )
    y_SS = np.sum((y_2 * y_2))

    Xy_sum = np.sum( X * y, axis=1 )

    r2 = (Xy_sum * Xy_sum / X_SS) / y_SS
    #print( np.min(X_SS), r2, file=sys.stderr)

    idx = np.argsort(r2)[-k:][::-1]
    return r2[ idx ], idx



def main():

    if (len(sys.argv)<3):
        print("Need gwas_id and position in hg19", file=sys.stderr)
        exit()


    gwas_snp = sys.argv[1]
    position = sys.argv[2]

    IDX, X, y = make_numpy_for_rsqaure( gwas_snp, position )
    if (len(y)==0):
        return
            
    val, idx = r_square_top_k(np.array(X), y, 30)
    top_list_r85 = idx[ val > 0.85 ]
    if (len(top_list_r85)<4):
        return
        
    for idx in top_list_r85:
        chrom, pos = IDX[ idx ]
        print ("chr%s\t%s\t%d\t%s" % (chrom, pos, int(pos)+1, gwas_snp ))

if __name__ == "__main__":
    main()
