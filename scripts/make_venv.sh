#! /bin/bash

scripts=`dirname "$0"`
base=$scripts/..

mkdir -p $base/venvs

python -m virtualenv -p <path-to-python-installation> <venv-name>

echo "To activate your environment:"
echo "    source $base/venvs/torch3/bin/activate"


