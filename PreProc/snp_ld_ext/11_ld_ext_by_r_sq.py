# coding: utf-8

import sys
import numpy as np
import tensorflow as tf



def make_numpy_for_rsqaure(gwas, pos):
    print ("processing %s in pos %s" % (gwas, pos), file=sys.stderr)

    index_l = list()
    numpy_l = list()

    fn = 'download/1kg.%s.vcf' % gwas
    
    with open(fn) as f:
        gwas_arr = list()
        for line in f:
            x = line.split(sep='\t')
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

    x_tf = tf.placeholder('float32', (None,None))
    y_tf = tf.placeholder('float32', (1,None))

    x_bar = tf.reduce_mean(x_tf, axis=1, keepdims=True)
    y_bar = tf.reduce_mean(y_tf, axis=1, keepdims=True)

    x_2 = x_tf - x_bar
    y_2 = y_tf - y_bar

    x_SS = tf.reduce_sum((x_2 * x_2), axis=1, keepdims=True)
    y_SS = tf.reduce_sum((y_2 * y_2), axis=1, keepdims=True)

    xy_sum = tf.matmul(x_2, y_2, transpose_b=True)

    r2_tf = xy_sum * xy_sum / x_SS / tf.transpose(y_SS)

    val_idx_tf = tf.nn.top_k( tf.reshape(r2_tf, [-1, ]), k=k )

    with tf.Session() as sess:
        Y = y.reshape(1,-1)
        val_idx = sess.run( val_idx_tf, feed_dict={x_tf: X, y_tf: Y})

    return val_idx


def main():

    if (len(sys.argv)<3):
        print("Need gwas_id and position in hg19", file=sys.stderr)
        exit()


    gwas_snp = sys.argv[1]
    position = sys.argv[2]

    IDX, X, y = make_numpy_for_rsqaure( gwas_snp, position )
    if (len(y)==0):
        return
            
    res = r_square_top_k(np.array(X), y, 30)
    top_list_r85 = res.indices[ res.values > 0.85 ]
    if (len(top_list_r85)<4):
        return
        
    for idx in top_list_r85:
        chrom, pos = IDX[ idx ]
        print ("chr%s\t%s\t%d\t%s" % (chrom, pos, int(pos)+1, gwas_snp ))

if __name__ == "__main__":
    main()
