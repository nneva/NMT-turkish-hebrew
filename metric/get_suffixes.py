import argparse
from collections import Counter, defaultdict
from itertools import groupby
import json
from pathlib import Path
import re

VOWELS = ['a', 'ı', 'o', 'u', 'e', 'i', 'ö', 'ü']

class TransAnalyser:
    """Class for analysis of suffixes in Turkish language."""

    def __init__(
        self,
        src_file,
        hyp_file,
        ref_file,
        train_file,
        suffix_file,
        suffixes=None
    ):
        self.src = Path(src_file).read_text().splitlines()
        self.hyp = Path(hyp_file).read_text().splitlines()
        assert len(self.hyp) == len(self.src), "Source and translated file must contain same number of lines."

        with open(suffix_file, "r") as f:
            self.suffix_dict = json.load(f)

        self.train = Path(train_file).read_text()
        self.ref = Path(ref_file).read_text().splitlines()
        assert len(self.ref) == len(self.src), "Source and reference file must contain same number of lines."

        if suffixes is not None:
            self.suffixes = suffixes
        else:
            self.suffixes = [s.strip() for s in set(self.suffix_dict.keys())]


    def get_frequency(self, suffix):
        frequency = Counter()
        frequency[suffix] = self.train.count(suffix)

        return frequency


    def extract_sents(self, suffix):
        hyps, refs = [], []

        for hyp, src, ref in zip(enumerate(self.hyp), enumerate(self.src), enumerate(self.ref)):
            if suffix in src[1]:
                hyps.append(hyp)
                refs.append(ref)

        return hyps, refs

    # bulid a pattern for the match of the suffixes 
    @staticmethod
    def _get_pattern(s_value):
        wspace = " "

        if wspace in s_value:
            return  "".join(e_ + ".*" for e_ in s_value.split())
        return s_value

    # pattern for checking whether personal noun is present for easier matching
    @staticmethod
    def _has_NNP(sent):

        return re.search(r"([A-Z][a-z]+)\s([A-Z][a-z]+)+", sent)

    # replace personal noun with the pronoun
    @staticmethod
    def _replace_NNP(s_value, sent):
        find_NNP = re.findall(r"([A-Z][a-z]+)\s([A-Z][a-z]+)+", sent)
        ppron = set(["he", "she", "it"])

        for NNP in find_NNP:
            sent.replace("".join(NNP), repr(ppron.intersection(set(s_value))))

        return sent


    def evaluate(self, suffix, hypothesis, references):
        c = Counter({"t_pos":0, "f_pos":0, "f_neg":0})
        true_pos, false_pos, false_neg = c.values()

        # in case that only one suffix is passed nargs retur str, list otherwise
        suff_value = [self.suffix_dict[suffix]] if not isinstance(self.suffix_dict[suffix], list) else [e for e in self.suffix_dict[suffix]]
        for elem in suff_value:
            pattern = self._get_pattern(elem)

            for (hyp_idx, hyp_sent), (ref_idx, ref_sent) in zip(hypothesis, references):
                match_hyp = re.search(rf"{pattern}", hyp_sent.lower())
                match_ref = re.search(rf"{pattern}", ref_sent.lower())

                if match_hyp and match_ref is None:
                    if self._has_NNP(ref_sent):
                        ref_sent = self._replace_NNP(elem, ref_sent)
                        if match_ref:
                            true_pos += 1
                    else:
                        false_pos += 1

                elif match_hyp is None and match_ref:
                    if self._has_NNP(hyp_sent):
                        hyp_sent= self._replace_NNP(elem, hyp_sent)
                        if match_hyp:
                            true_pos += 1
                    else:
                        false_neg += 1
                else:
                    true_pos += 1
        try:
            
            P = round(true_pos/(true_pos + false_pos), 3)
            R = round(true_pos/(true_pos + false_neg), 3)
            F1 = round(2 * ((P * R)/(P + R)), 3)

        except ZeroDivisionError:
            P = 0
            R = 0
            F1 = 0

        return P, R, F1


class SegMatcher:
    "Class for matching the pattern of a given suffix."

    def __init__(self, seg_file, suffixes) -> None:
        self.BPE = Path(seg_file).read_text()
        self.alomorphs = self.get_alomorphs(suffixes)

    # get all variants of the same suffix in groups; e.g. sünüz & sunuz
    def get_alomorphs(self, suffixes):
        alomorphs = defaultdict(list)

        for key, group in groupby(suffixes, lambda s: [char for char in s if char not in VOWELS]):
            key = "".join(key)
            alomorphs[key] += (list(group))

        return alomorphs
    
    # search through all possible positios of @@ relative to the suffix; e.g @@ sunuz, s@@ uuz, su@@ nuz etc.
    def get_patterns(self):
        patterns = dict()
        for key, group in self.alomorphs.items():
            patterns[key] = {}
            for suffix in group:
                patterns[key][suffix] = {}
                count = self.BPE.count(suffix)
                patterns[key][suffix][suffix] = count

                for i in range(1, len(suffix)):
                    bpe_suffix = suffix[:i] + "@@ " + suffix[i:]
                    count = self.BPE.count(bpe_suffix)
                    patterns[key][suffix][bpe_suffix] = count

        return patterns


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-s",
        "--src-file",
        type=str,
        required=True,
        help="Path to source language test file."
    )
    parser.add_argument(
        "-r",
        "--ref-file",
        type=str,
        required=True,
        help="Path to reference test file."
    )
    parser.add_argument(
        "-hyp",
        "--hyp-file",
        type=str,
        required=True,
        help="Path to translated test file."
    )
    parser.add_argument(
        "-t",
        "--train-file",
        type=str,
        required=True,
        help="Path to source language train file."
    )
    parser.add_argument(
        "-sf",
        "--suffix-file",
        type=str,
        required=True,
        help="Path to suffix JSON file."
    )
    parser.add_argument(
        "-seg",
        "--seg-file",
        type=str,
        help="Path to subword segmented test file."
    )
    parser.add_argument(
        "-suf",
        "--suffixes",
        type=str,
        nargs="*",
        help="Suffix(es) to examine."
    )

    args = parser.parse_args()

    analyser = TransAnalyser(
        src_file=args.src_file,
        ref_file=args.ref_file,
        hyp_file=args.hyp_file,
        train_file=args.train_file,
        suffixes=args.suffixes,
        suffix_file=args.suffix_file
    )

    p, r, f1 = 0, 0, 0

    segMatcher = SegMatcher(args.seg_file, analyser.suffix_dict.keys())
    patterns = segMatcher.get_patterns()

    for s in analyser.suffixes:
        hypotheses, references = analyser.extract_sents(s)
        frequency = analyser.get_frequency(s)
        score = analyser.evaluate(s, hypotheses, references)
        print(f"Raw frequency of the suffix '{s}' in train is: {frequency.total()}.")
        print(f"Results for suffix: {s} Precision: {score[0]}. Recall: {score[1]}. F1: {score[2]} ")
        for key in patterns:
            if s in patterns[key]:
                print(f"Most used patterns of suffix {s}")
                print(patterns[key][s])
                break

        p += score[0]
        r += score[1]
        f1 += score[2]
        print()

    l = len(analyser.suffixes)
    avg_p = p/l
    avg_r = r/l
    avg_f1 = f1/l
    print(f"Precision per model is:'{round(avg_p, 3)}'. \
            Recall per model is: '{round(avg_r, 3)}'. \
            F1 per model is: '{round(avg_f1)}'.")


if __name__ == "__main__":
    main()

