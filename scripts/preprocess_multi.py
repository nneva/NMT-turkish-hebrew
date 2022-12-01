import argparse

VOWELS = "aeuioöuüıAEUOÖUÜIİ"

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--input-src", type=str,
                        help="Path to tokenized text file.")
    parser.add_argument("--input-src-bpe", type=str,
                        help="Path to bpe modified file.", required=True)
    parser.add_argument("--src-output", type=str,
                        help="Path to output file.", required=True)
    parser.add_argument("--separator", type=str,
                        help="Separator between sentences.", required=True)
    parser.add_argument("--special-symbol", type=str,
                        help="Special symbol to replace vowels.")

    args = parser.parse_args()

    return args

def modify_all(line: str, special_symbol: str):
    
    replace_vowels = str.maketrans({char: special_symbol for char in VOWELS})

    return line.translate(replace_vowels)


def main():
    args = parse_args()
    path_to_file = args.input_src

    if args.input_src:
        with open(path_to_file, "r", encoding="utf-8") as t_file, \
            open(args.input_src_bpe, "r", encoding="utf-8") as bpe_file, \
            open(args.src_output, "w", encoding="utf-8") as out_file:
            for  bpe_line, t_line in zip(bpe_file.readlines(), t_file.readlines()):
                line = bpe_line.rstrip()  + args.separator + t_line.rstrip()
                out_file.write(line + "\n")

    else:
        with open(args.input_src_bpe, "r", encoding="utf-8") as bpe_file, \
            open(args.src_output, "w", encoding="utf-8") as out_file:
            for  bpe_line in bpe_file.readlines():
                line = bpe_line.rstrip()  + args.separator + bpe_line.rstrip()
                out_file.write(line + "\n")

    
if __name__ == "__main__":
    main()