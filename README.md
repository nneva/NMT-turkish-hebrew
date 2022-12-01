# NMT for Hebrew and Turkish

This repo is just a collection of scripts showing how to download
data and train & evaluate models with [JoeyNMT](https://github.com/joeynmt/joeynmt),
using different approaches.

- on a BPE-level ( + BPE-dropout )
- on a character-level
- with multi-encoder approah

Language directions:

- TR -> EN
- HE -> EN

# Requirements

- This only works on a Unix-like system, with bash.
- Python 3 must be installed on your system, i.e. the command `python3` must be available
- Make sure virtualenv is installed on your system. 

**Important**: In all scripts and configs paths need to be changed accoridingly. 

# Steps

💻 Create a new virtualenv that uses Python 3. 

    ./scripts/make_virtualenv.sh

**Important**: Then activate the env by executing the `source` command that is output by the shell script above.

🛠️ Download and install required software:

    ./scripts/install_requirements.sh


⬇️ Download data:

    ./scripts/prepare_data.sh


This script will download the data for the training and subsample it to train, dev & test.

The data is not preprocessed, as it is done internally by Joey NMT. See configs/data for more details.


📗 Learn BPE and save vocabs:

    ./scripts/learn_bpe.sh


Special preprocessing steps that are not done by Joey NMT:

🆑 Preprocess data for the character-level parent model training:

    python scripts/preprocess_char.py <input file path> <output file path>


🆑 Preprocess data for the character-level finetuning:

    ./scripts/preprocess_char.sh


✂️ Preprocess data for the multi-encoder approach:

    ./scripts/preprocess_multi.sh


🅰️ Preprocess data for the vowel replacement in Hebrew:

    ./scripts/prepare_he.sh


🅰️ Preprocess test data for the vowel replacement in Hebrew. This is done before the translation:

    ./scripts/prepare_test.sh


🤸 Train a model:

    ./scripts/train.sh

The training process can be interrupted at any time, and the best checkpoint will always be saved.


📝 Translate a trained model with:

    ./scripts/translate.sh

This script will create directory `translations`, with the subdirectory named after the model.


 ✂️ Post-processing step needed for multi-encoder approach. This is done before the evaluation:

    ./scripts/postprocess_multi.sh


📝 Evaluate trained models with:

    ./sacrebleu <path to references> -i <path to translation file> -m bleu

    ./bert-score -r <path to references> -c <path to translation file> --lang en --resale_with_baseline --num_layers 19

    ./scripts/evaluate.sh

Results of the evaluation will be printed out in the terminal.

    ./scripts/evaluate.sh 
    
will additionlly print the segmentation patterns for each of the suffixes

