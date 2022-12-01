import argparse


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()

    parser.add_argument("--src-file", type=str, help="Path to source text file.", required=True)
    parser.add_argument("--trg-file", type=str, help="Path to target text file.", required=True)
    parser.add_argument("--src-train", type=str, help="Path to source sample file.", required=True)
    parser.add_argument("--src-dev", type=str, help="Path to source sample file.", required=True)
    parser.add_argument("--src-test", type=str, help="Path to source sample file.", required=True)
    parser.add_argument("--trg-train", type=str, help="Path to target sample file.", required=True)
    parser.add_argument("--trg-dev", type=str, help="Path to target sample file.", required=True)
    parser.add_argument("--trg-test", type=str, help="Path to target sample file.", required=True)
    parser.add_argument("--num-lines", type=int, help="Desired number of lines.", required=True)

    args = parser.parse_args()

    return args

def subsample_sents(src_file, trg_file, src_new, trg_new, num_lines, used_nums):
    n = 0
    sent_src_to_write, sent_trg_to_write = [], []
    for (idx_src, sent_src), (_, sent_trg) in zip(enumerate(src_file, start=1), enumerate(trg_file, start=1)):
        if idx_src not in used_nums:
            sent_src_to_write.append(sent_src)
            sent_trg_to_write.append(sent_trg)
            used_nums.append(idx_src)
            n += 1
            if n >= num_lines:
                break

    with open(src_new, "w", encoding="utf-8") as src_out, open(trg_new, "w", encoding="utf-8") as trg_out:
        src_out.writelines(sent_src_to_write)
        trg_out.writelines(sent_trg_to_write)

def main():
    used_nums = []
    args = parse_args()

    with open(args.src_file, "r", encoding="utf-8") as src, open(args.trg_file, "r", encoding="utf-8") as trg:
        source, target = src.readlines(), trg.readlines()
        assert len(source) == len(target), "Both files must contain same number of lines."

        if args.src_train and args.trg_train:
            subsample_sents(source, target, args.src_train, args.trg_train, args.num_lines, used_nums)
        if args.src_dev and args.trg_dev:
            subsample_sents(source, target, args.src_dev, args.trg_dev, args.num_lines // 7, used_nums)
        if args.src_test and args.trg_test:
            subsample_sents(source, target, args.src_test, args.trg_test, args.num_lines // 5, used_nums)

if __name__ == "__main__":
    main()