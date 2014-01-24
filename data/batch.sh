#!/bin/bash

FILE=$1
NUM=$2
HALF=$(( $NUM / 2 ))
SPLITS=$3

# preprocess
discodop treetransforms binarize $FILE $FILE.$NUM.bin --inputfmt=bracket --outputfmt=bracket --ensureroot=TOP --functions=remove -h 1 -v 1 --slice=0:$NUM

# Split in $SPLITS random ways
for i in `seq 1 $SPLITS`;
do
	# Random sort and split
	cat $FILE.$NUM.bin | gsort -R | split -l $HALF - $FILE.split$HALF.$i.

	# aa = HC, ab = EC

	# double-dop
	discodop fragments $FILE.split$HALF.$i.aa $FILE.split$HALF.$i.ab --cover --relfreq > $FILE.split$HALF.$i.mo.txt

	# dop-star
	discodop grammar dopreduction $FILE.split$HALF.$i.ab $FILE.split$HALF.$i.EC --inputfmt=bracket --gzip --dopestimator=shortest

	python dopstar.py $FILE.split$HALF.$i.EC.rules.gz $FILE.split$HALF.$i.EC.lex.gz $FILE.split$HALF.$i.aa --relfreq -s TOP >$FILE.split$HALF.$i.sd.txt

done

# double-dop (all)
discodop fragments $FILE.$NUM.bin --cover --relfreq > $FILE.$NUM.mo.txt

# dop-star all -- INCORRECT
discodop grammar doubledop $FILE.$NUM.bin $FILE.$NUM.ddop --inputfmt=bracket --gzip --dopestimator=shortest
python dopstar.py $FILE.$NUM.ddop.rules.gz $FILE.$NUM.ddop.lex.gz $FILE.$NUM.bin --relfreq -s TOP >$FILE.$NUM.sd.txt