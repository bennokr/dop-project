
# preprocess split
discodop treetransforms binarize ORIGINAL_READABLE_CLEANED/wsj-02-21.mrg wsj500EC.mrg --inputfmt=bracket --outputfmt=bracket --ensureroot=TOP --functions=remove -h 1 -v 1 --slice=0:500
discodop treetransforms binarize ORIGINAL_READABLE_CLEANED/wsj-02-21.mrg wsj500HC.mrg --inputfmt=bracket --outputfmt=bracket --ensureroot=TOP --functions=remove -h 1 -v 1 --slice=500:1000

# double-dop split
discodop fragments wsj500HC.mrg wsj500EC.mrg --cover --relfreq >wsj_ddop_split_500_500_1.txt

# dop-star (split)
discodop grammar dopreduction wsj500EC.mrg wsj500EC --inputfmt=bracket --gzip --dopestimator=shortest
python ../dopstar.py wsj500EC.rules.gz wsj500EC.lex.gz wsj500HC.mrg --relfreq -s TOP >wsj_dops_split_500_500_1.txt


# preprocess all
discodop treetransforms binarize ORIGINAL_READABLE_CLEANED/wsj-02-21.mrg wsj1000.mrg --inputfmt=bracket --outputfmt=bracket --ensureroot=TOP --functions=remove -h 1 -v 1 --slice=0:1000

# double-dop (all)
discodop fragments wsj1000.mrg --cover --relfreq >wsj_ddop_1vall_1000_1.txt

# dop-star all
discodop grammar doubledop wsj1000.mrg wsj1000 --inputfmt=bracket --gzip --dopestimator=shortest
python ../dopstar.py wsj1000.rules.gz wsj1000.lex.gz wsj1000.mrg --relfreq -s TOP >wsj_dops_1vall_1000_1.txt