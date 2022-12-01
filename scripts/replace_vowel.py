import argparse


VOWELS = "aeuioöuüıAEUOÖUÜIİ"

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--input-file", type=str, help="Path to input text file.", required=True)
    parser.add_argument("--output-file", type=str, help="Path to modified output file.", required=True)
    parser.add_argument("--symbol", type=str, help="Special symbol to replace vowels.", required=True)

    args = parser.parse_args()

    return args


def modify_all(line: str, symbol: str, ):
    
    replace_vowels = str.maketrans({char: symbol for char in VOWELS})
    
    return line.translate(replace_vowels)


def modify_no_root(line: str, symbol: str):
    line_ = ""

    for token in line.split():
        replace_vowels = str.maketrans(token[3:], modify_all(token[3:], symbol))
        token_ = token[:3] + token[3:].translate(replace_vowels) + " "
        line_ += token_

    return line_


def main():
    args = parse_args()
    input_f = args.input_file

    if "vocab" not in input_f:
        with open(input_f, "r", encoding="utf-8") as in_file, open(args.output_file, "w", encoding="utf-8") as out:
            for line in in_file:
                new_line = modify_all(line, args.symbol)
                out.write(new_line)
    else:
        with open(input_f, "r", encoding="utf-8") as in_file, open(args.output_file, "w", encoding="utf-8") as out:
            for line in in_file:
                new_line = modify_all(line, args.symbol) if "@@" in line else line
                out.write(new_line)


if __name__ == "__main__":
    main()