discodop treetransforms binarize tiny.mrg ECtiny.mrg --inputfmt=bracket --outputfmt=bracket --ensureroot=TOP --functions=remove -h 1 -v 1 --slice=0:3
discodop treetransforms binarize tiny.mrg HCtiny.mrg --inputfmt=bracket --outputfmt=bracket --ensureroot=TOP --functions=remove -h 1 -v 1 --slice=3:
discodop fragments HCtiny.mrg ECtiny.mrg --cover --relfreq >tiny-ddop-frags.txt
discodop grammar dopreduction ECtiny.mrg ECtiny --inputfmt=bracket --gzip --dopestimator=shortest
python fragsinshortestderivs.py ECtiny.rules.gz ECtiny.lex.gz HCtiny.mrg --relfreq -s TOP >tiny-dopstar-frags.txt
