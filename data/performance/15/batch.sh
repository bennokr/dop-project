#!/bin/sh
discodop treetransforms none wsj-24.mrg wsj-24-len15.mrg \
		--inputfmt=bracket --outputfmt=bracket --maxlen=15
discodop treetransforms none wsj-24.mrg wsj-24-len15-wordpos.txt \
		--inputfmt=bracket --outputfmt=wordpos --maxlen=15

for GRAMMAR in dops ddop-split ddop
do
	discodop parser $GRAMMAR.rules.gz $GRAMMAR.lex.gz \
			wsj-24-len15-wordpos.txt --bt=$GRAMMAR.backtransform.gz \
			-z --tags --mpp=1000 -s TOP --numproc=16 \
		| discodop treetransforms unbinarize \
			--inputfmt=discbracket --outputfmt=bracket >$GRAMMAR.results \
	&& discodop eval --goldfmt=bracket --parsesfmt=bracket \
		wsj-24-len15.mrg $GRAMMAR.results COLLINS.prm >$GRAMMAR.eval.txt \
	|| exit $?
done

