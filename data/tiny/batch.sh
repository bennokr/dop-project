
# preprocess split
discodop treetransforms binarize tiny.mrg tinyEC.mrg --inputfmt=bracket --outputfmt=bracket --ensureroot=TOP --functions=remove -h 1 -v 1 --slice=0:3
discodop treetransforms binarize tiny.mrg tinyHC.mrg --inputfmt=bracket --outputfmt=bracket --ensureroot=TOP --functions=remove -h 1 -v 1 --slice=3:

# double-dop split
discodop fragments tinyHC.mrg tinyEC.mrg --cover --relfreq >tiny_ddop_split_3_4_1.txt

# dop-star (split)
discodop grammar dopreduction tinyEC.mrg tinyEC --inputfmt=bracket --gzip --dopestimator=shortest
python ../dopstar.py tinyEC.rules.gz tinyEC.lex.gz tinyHC.mrg --relfreq -s TOP >tiny_dops_split_3_4_1.txt


# preprocess all
discodop treetransforms binarize tiny.mrg tinyBIN.mrg --inputfmt=bracket --outputfmt=bracket --ensureroot=TOP --functions=remove -h 1 -v 1

# double-dop (all)
discodop fragments tinyBIN.mrg --cover --relfreq >tiny_ddop_1vall_7_1.txt

# dop-star all
discodop grammar doubledop tinyBIN.mrg tiny --inputfmt=bracket --gzip --dopestimator=shortest
python ../dopstar.py tiny.rules.gz tiny.lex.gz tinyBIN.mrg --relfreq -s TOP >tiny_dops_1vall_7_1.txt