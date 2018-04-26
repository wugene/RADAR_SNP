#/usr/bin/python3

# coding: utf-8
from pyliftover import LiftOver
import sys

if (len(sys.argv)<2):
    print("Need filename in coordinate hg38")
    exit()


lo = LiftOver('hg38', 'hg19')
fn = sys.argv[1]

with open(fn) as f:
  for x in f.readlines():
    x_l = x.split('\t')
    x_con = lo.convert_coordinate('chr'+x_l[0], int(x_l[1])-1)
    if (len(x_con)>0):
      print ( "%s\t%d\t%d\t%s" % (x_con[0][0], x_con[0][1], x_con[0][1]+1, x_l[2]) )
    else:
      print ("Skip one line", x, file=sys.stderr)
