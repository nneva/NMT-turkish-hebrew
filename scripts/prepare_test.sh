#! /bin/bash
scripts=`dirname "$0"`
base=$scripts/..
data=$base/data

src=he
trg=en
lang=en-he


# remove empty lines from the test data
mv $data/raw/test.en-he.$src $data/raw/test.en-he.ws.$src

python scripts/del_spaces.py --file-in $data/raw/test.en-he.ws.$src --file-out $data/raw/test.en-he.$src

rm $data/raw/test.en-he.ws.$src