#!/bin/sh
 
# split treebank in HC & EC
discodop treetransforms binarize ../wsj/ORIGINAL_READABLE_CLEANED/wsj-02-21.mrg EC.mrg --inputfmt=bracket --outputfmt=bracket --ensureroot=TOP --functions=remove -h 1 -v 1 --slice=0:20000
discodop treetransforms binarize ../wsj/ORIGINAL_READABLE_CLEANED/wsj-02-21.mrg HC.mrg --inputfmt=bracket --outputfmt=bracket --ensureroot=TOP --functions=remove -h 1 -v 1 --slice=20000:
 
# get DOP reduction for EC
time discodop grammar dopreduction EC.mrg EC --inputfmt=bracket --gzip --dopestimator=shortest
 
# collect shortest derivations of HC trees with DOP reduction of EC
time python dopstar.py EC.rules.gz EC.lex.gz HC.mrg --relfreq -s TOP --numproc=12 >dopstarfrags.txt