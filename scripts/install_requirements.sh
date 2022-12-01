#! /bin/bash
scripts=`dirname "$0"`
base=$scripts/..

pip uninstall setuptools
pip install setuptools==59.5.0
pip install torchtext==0.11.2
pip install sacrebleu==2.0.0
pip install subword-nmt==0.3.8
pip install joeynmt==2.0.0
pip install virtualenv
pip install sacremoses
pip install bert-score

