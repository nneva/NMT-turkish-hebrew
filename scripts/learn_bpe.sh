#! /bin/bash
scripts=`dirname "$0"`
base=$scripts/..

data=$base/data
shared_models=$base/shared_models

src=? # tr or he
trg=en
lang=? # en-tr or en-he 

model_name=?

mkdir -p $shared_models
mkdir -p $shared_models/$model_name


subword-nmt learn-joint-bpe-and-vocab --input $data/$model_name/train.$lang.$src $data/$model_name/train.$lang.$trg \
            --write-vocabulary $base/shared_models/$model_name/vocab_raw.$src $base/shared_models/$model_name/vocab_raw.$trg  \
            -s 7000 --total-symbols -o $base/shared_models/$model_name/$src$trg.bpe

# removing counts from the bpe vocab files because Joey NMT just reads in the files without striping the counts

cat $shared_models/$model_name/vocab_raw.$src | python scripts/get_vocab.py --vocab-in $shared_models/$model_name/vocab_raw.$src --vocab-out $shared_models/$model_name/vocab.$src
cat $shared_models/$model_name/vocab_raw.$trg | python scripts/get_vocab.py --vocab-in $shared_models/$model_name/vocab_raw.$trg --vocab-out $shared_models/$model_name/vocab.$trg

rm $shared_models/$model_name/vocab_raw.$src
rm $shared_models/$model_name/vocab_raw.$trg