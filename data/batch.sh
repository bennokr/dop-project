#!/bin/bash

FILE=$1
OUT=$2
NUM=$3
HALF=$(( $NUM / 2 ))
SPLITS=$4

# preprocess
discodop treetransforms binarize $FILE $OUT.$NUM.bin --inputfmt=bracket --outputfmt=bracket --ensureroot=TOP --functions=remove -h 1 -v 1 --slice=0:$NUM

# Split in $SPLITS random ways
for i in `seq 1 $SPLITS`;
do
	# Random sort and split
	cat $OUT.$NUM.bin | gsort -R | split -l $HALF - $OUT.split$HALF.$i.

	# aa = HC, ab = EC

	# double-dop
	discodop fragments $OUT.split$HALF.$i.aa $OUT.split$HALF.$i.ab --cover --relfreq > $OUT.split$HALF.$i.mo.txt

	# dop-star
	discodop grammar dopreduction $OUT.split$HALF.$i.ab $OUT.split$HALF.$i.EC --inputfmt=bracket --gzip --dopestimator=shortest

	python dopstar.py $OUT.split$HALF.$i.EC.rules.gz $OUT.split$HALF.$i.EC.lex.gz $OUT.split$HALF.$i.aa --relfreq -s TOP >$OUT.split$HALF.$i.sd.txt

done

# double-dop (all)
discodop fragments $OUT.$NUM.bin --cover --relfreq > $OUT.$NUM.mo.txt

# dop-star all -- INCORRECT
# discodop grammar doubledop $OUT.$NUM.bin $OUT.$NUM.ddop --inputfmt=bracket --gzip --dopestimator=shortest
# python dopstar.py $OUT.$NUM.ddop.rules.gz $OUT.$NUM.ddop.lex.gz $OUT.$NUM.bin --relfreq -s TOP >$OUT.$NUM.sd.txt