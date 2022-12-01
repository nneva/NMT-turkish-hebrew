#! /bin/bash
scripts=`dirname "$0"`
base=$scripts/..


python metric/get_suffixes.py --src-file metric/data/source.tr --ref-file metric/data/reference.en --hyp-file metric/data/translation.txt --train-file metric/data/train.en-tr.tr \
                --seg-file metric/data/source_bpe_segmented.tr --suffix-file metric/data/TurkishSuffix.json --suffixes alım siniz tuğ sunuz dük umuz 

# sample files are in directory metric/data