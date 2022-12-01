#! /bin/bash
scripts=`dirname "$0"`
base=$scripts/..
data=$base/data
shared_models=$base/shared_models
model_name=BPE_7k

src=he
trg=en
lang=en-he


# replace vowels
list=( dev test train )

for i in "${list[@]}"; do
    python scripts/replace_vowel.py --input-file "$data/raw/$i.$lang.$src" --output-file "$data/raw/$i.$lang.repl_v.$src" --symbol "+"
done


# rename target data
for j in "${list[@]}"; do
    mv "$data/raw/$j.$lang.$trg" "$data/raw/$j.$lang.repl_v.$trg"
done

# get vocab
python scripts/replace_vowel.py --input-file "$shared_models/$model_name/vocab.$src" --output-file "$shared_models/$model_name/vocab.repl_v.$src" --symbol "+"

python scripts/replace_vowel.py --input-file "$shared_models/$model_name/heen.bpe" --output-file "$shared_models/$model_name/heen.repl_v.bpe" --symbol "+"

mv $shared_models/$model_name/vocab.$trg $shared_models/$model_name/vocab.repl_v.$trg

