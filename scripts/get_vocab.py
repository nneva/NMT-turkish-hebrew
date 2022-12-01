import argparse


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()

    parser.add_argument("--vocab-in", type=str, help="Path to source text file.", required=True)
    parser.add_argument("--vocab-out", type=str, help="Path to source text file.", required=True)

    args = parser.parse_args()

    return args


def main():
    args = parse_args()

    with open(args.vocab_in, "r", encoding="utf-8") as vocab_in, open(args.vocab_out, "w", encoding="utf-8") as vocab_out:
        for line in vocab_in:
            line = line.split()
            vocab_out.write(line[0] + "\n")
    
    
if __name__ == "__main__":
    main()