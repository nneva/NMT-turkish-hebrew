#! /bin/bash
scripts=`dirname "$0"`
base=$scripts/..

data=$base/data
tr=$data/en-tr
he=$data/en-he

langt=en-tr
langh=en-he

srct=tr
src=he
trg=en

mkdir -p $data

# Download data
wget https://opus.nlpl.eu/download.php?f=SETIMES/v2/moses/en-tr.txt.zip -O $base/en-tr.zip && unzip $base/en-tr.zip -d $tr
wget https://object.pouta.csc.fi/OPUS-TED2020/v1/moses/en-he.txt.zip -O $base/en-he.zip && unzip $base/en-he.zip -d $he

rm $base/en-tr.zip
rm $base/en-he.zip
echo "Data downloaded and extracted."

raw=$tr/raw
mkdir -p $raw

echo "Splitting TR-EN data into train, dev and test sets."
echo "This may take a while..."
python scripts/subsample.py --src-file $tr/SETIMES.$langt.$srct --trg-file $tr/SETIMES.$langt.$trg \
--src-train $raw/train.$langt.$srct --src-dev $raw/dev.$langt.$srct --src-test $raw/test.$langt.$srct \
--trg-train $raw/train.$langt.$trg --trg-dev $raw/dev.$langt.$trg --trg-test $raw/test.$langt.$trg \
--num-lines 150000
echo "TR-EN data split."

hraw=$he/raw
mkdir -p $hraw

echo "Splitting HE-EN data into train, dev and test sets."
echo "This may take a while..."
python scripts/subsample.py --src-file $he/TED2020.$langh.$srch --trg-file $he/TED2020.$langh.$trg \
--src-train $hraw/train.$langh.$srch --src-dev $hraw/dev.$langh.$srch --src-test $hraw/test.$langh.$srch \
--trg-train $hraw/train.$langh.$trg --trg-dev $hraw/dev.$langh.$trg --trg-test $hraw/test.$langh.$trg \
--num-lines 150000
echo "HE-EN data split."




