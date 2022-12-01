#! /bin/bash

scripts=`dirname "$0"`
base=$scripts/..
data=$base/data
tools=$base/tools
shared_models=$base/shared_models
bpe_char=$data/bpe_char_tokenized

src=tr
trg=en
lang=en-tr

char_dir=$data/char
vocab_dir=$shared_models/trf_char

mkdir -p $char_dir
mkdir -p $vocab_dir

# prepare data for char-level finetuning
for f in $bpe_char/dev.$lang $bpe_char/test.$lang $bpe_char/train.$lang; do
    for l in $src $trg; do
        cat $f.$l | sed -e 's/ //g;s/▁/ /g;s/^ //'>  $char_dir/${f#$(dirname $f)/}.$l
    done
done






