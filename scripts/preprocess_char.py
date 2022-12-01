#!/usr/bin/env python
import argparse
import sys
import unicodedata

""" Adapted implementation of a toknizer from https://github.com/jlibovicky/char-nmt.git as described in:
    
        [Towards Reasonably-Sized Character-Level Transformer NMT by Finetuning Subword Systems](https://aclanthology.org/2020.emnlp-main.203) 
        (Libovický & Fraser, EMNLP 2020).
"""
SPACE = "▁"

ALNUM_CHARSET = set(chr(i) for i in range(sys.maxunicode)
                if (unicodedata.category(chr(i)).startswith("L")
                or unicodedata.category(chr(i)).startswith("N")))


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--input-file", type=str, help="Path to input text file.", required=True)
    parser.add_argument("--output-file", type=str, help="Path to input text file.", required=True)

    args = parser.parse_args()

    return args


def tokenize(line: str) -> str:
    """Tokenize line such that all words containing only alphanumeric characters are preceded with ▁, 
        Words containing non-alphanumeric characters are split on token(s) containing only alphanumeric characters preceded with ▁,
        and token(s) containing non-alphanumeric character(s) preceded with whitespace.
        :param line: Single line of input text as string.
        :return: Tokenized line.
    """
    tokens = []

    for token in line.strip().split(" "):
        chars = set((char for char in token))
        alphanums = chars.intersection(ALNUM_CHARSET)
        non_alphanums = chars - alphanums
        
        if len(chars) == len(alphanums):
            tokens.append(SPACE + token)
        
        elif len(chars) == len(non_alphanums):
            tokens.append(" " + token)

        else:
            new_token = ""
            get_prefix = lambda new_token: " " if new_token[-1] in non_alphanums else SPACE

            for char in token:
                if len(new_token) == 0 \
                    or (char in alphanums and new_token[-1] in alphanums) \
                    or (char in non_alphanums and new_token[-1] in non_alphanums):
                    new_token += char
                else:
                    tokens.append(get_prefix(new_token) + new_token)
                    new_token = char
            
            tokens.append(get_prefix(new_token) + new_token)


    return  " ".join(tokens)


def main():
    args = parse_args()
    
    with open(args.input_file, "r", encoding="utf-8") as current, open(args.output_file, "w", encoding="utf-8") as out:
        for line in current:
            line = tokenize(line)
            out.write(line + "\n")


if __name__ == "__main__":
    main()