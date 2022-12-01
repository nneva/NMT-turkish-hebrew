#! /bin/bash
scripts=`dirname "$0"`
base=$scripts/..
data=$base/data
shared_models=$data/shared_models

src=tr
trg=en
lang=en-tr

raw=$data/$lang/raw
replaced_vowels=$data/replaced_vowels
multi=$data/multi

mkdir -p $replaced_vowels
mkdir -p $multi
mkdir -p $shared_models/MULTI


for f in $raw/dev.$lang.$src $raw/test.$lang.$src $raw/train.$lang.$src; do
    python scripts/replace_vowel.py --input-file $f --output-file $replaced_vowels/${f#$(dirname $f)/} --symbol "+"
done

for f in $replaced_vowels/dev.$lang $replaced_vowels/test.$lang $replaced_vowels/train.$lang; do
    python scripts/preprocess_multi.py --input-src $f.$src --input-src-bpe $raw/${f#$(dirname $f)/}.$src --src-output data/multi/${f#$(dirname $f)/}.$src --separator " ??? " 
done

for f in $raw/dev.$lang $raw/test.$lang $raw/train.$lang; do
    python scripts/preprocess_multi.py  --input-src-bpe $f.$trg --src-output data/multi/${f#$(dirname $f)/}.$trg --separator " ??? " 
done

