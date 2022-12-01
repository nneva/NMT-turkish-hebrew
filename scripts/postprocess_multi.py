import argparse

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--input-file", type=str,
                        help="Path to the hypothesis file.")
    parser.add_argument("--output-file", type=str,
                        help="Path to output file.", required=True)
    parser.add_argument("--separator", type=str,
                        help="Separator between the sentences.", required=True)

    args = parser.parse_args()

    return args


def main():
    args = parse_args()

    with open(args.input_file, "r", encoding="utf-8") as in_file, open(args.output_file, "w", encoding="utf-8") as out_file:
        for in_line in in_file:
            line = in_line.rstrip().split(args.separator) 
            out_file.write(line[0] + "\n")

if __name__ == "__main__":
    main()