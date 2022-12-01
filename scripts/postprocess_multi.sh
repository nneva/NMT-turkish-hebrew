#! /bin/bash
scripts=`dirname "$0"`
base=$scripts/..
models=$base/models
data=$base/data
configs=$base/configs

translations=$base/translations

lang=en-tr
src=tr
trg=en

num_threads=51200
device=0

model_name=MULTI
mkdir -p $translations/$model_name


python scripts/postprocess_multi.py --input-file $translations/MULTI/test.$lang.$trg --output-file $translations/MULTI/test.$lang.umerge.$trg --separator="???"

# used in case that there are some residuals from moses; pattern can vary
sed -r "s/ &apos<unk> /'/g" translations/MULTI/test.$lang.umerge.$trg > $translations/MULTI/test.$trg



