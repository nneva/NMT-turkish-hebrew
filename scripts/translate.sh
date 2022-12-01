#! /bin/bash
scripts=`dirname "$0"`
base=$scripts/..

data=$base/data
configs=$base/configs
translations=$base/translations

src=? # tr or he
trg=en
lang=? # en-tr or en-he

num_threads=51200
device=0
SECONDS=0

mkdir -p $translations
model_name=?
data_sub=$data/$lang

echo "###############################################################################"
echo "model_name $model_name"
echo "###############################################################################"

translations_sub=$translations/$model_name

mkdir -p $translations_sub


CUDA_VISIBLE_DEVICES=$device OMP_NUM_THREADS=$num_threads python -m joeynmt translate $configs/$model_name.yaml < $data_sub/test.$lang.$src > $translations_sub/test.$lang.$trg


echo "time taken:"
echo "$SECONDS seconds"
