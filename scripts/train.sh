#! /bin/bash
scripts=`dirname "$0"`
base=$scripts/..

models=$base/models
configs=$base/configs
logs=$base/logs
data=$base/data

src=? # tr or he
trg=en
lang=? # en-tr or en-he

num_threads=51200
device=0

model_name=?

mkdir -p $logs/$model_name
#mkdir -p $models 


echo "train..."
CUDA_VISIBLE_DEVICES=$device OMP_NUM_THREADS=$num_threads python -m joeynmt train $configs/$model_name.yaml > $logs/$model_name/out 2> $logs/$model_name/err 
