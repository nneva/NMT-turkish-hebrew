import argparse


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()

    parser.add_argument("--file-in", type=str, help="Path to source text file.", required=True)
    parser.add_argument("--file-out", type=str, help="Path to source text file.", required=True)

    args = parser.parse_args()

    return args


def main():
    args = parse_args()

    with open(args.file_in, "r", encoding="utf-8") as file_in, open(args.file_out, "w", encoding="utf-8") as file_out:
        for line in file_in:
            if line.startswith("\n"):
                del line
            else:
                file_out.write(line)
    
    
if __name__ == "__main__":
    main()