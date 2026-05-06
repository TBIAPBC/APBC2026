import argparse
import random
import sys
import textwrap


def read_input(inputfile, mode):
    with open(inputfile, "rt") as f:
        text = f.read()

    text = " ".join(text.split())

    if mode == "words":
        return text.split()
    return list(text)

def build_sa(tokens):
    suffixes = []
    for start in range(len(tokens)):
        suffix = tuple(tokens[start:])
        print(start, suffix)
        suffixes.append((suffix, start))
    suffixes.sort() # sort lexicographically
    return [start for suffix, start in suffixes] # just collect the start index

def left_bound(sa, tokens, pattern):
    """ find lower bound with binary search for matching pattern """
    lo, hi = 0, len(sa)
    plen = len(pattern)
    while lo < hi:
        mid = (lo + hi) // 2
        if tuple(tokens[sa[mid]:sa[mid]+plen]) < pattern: # works since sa has lexographic order
            lo = mid + 1
        else:
            hi = mid
    return lo

def right_bound(sa, tokens, pattern):
    """ find upper bound with binary search for matching pattern """
    lo, hi = 0, len(sa)
    plen = len(pattern)
    while lo < hi:
        mid = (lo + hi) // 2
        if tuple(tokens[sa[mid]:sa[mid]+plen]) <= pattern:  # check if slice is still smaller or equal pattern
            lo = mid + 1                                    # if yes try one more right
        else:
            hi = mid                                        # if no look in smaller half
    return lo

def continuations(sa, tokens, pattern):
    lo = left_bound(sa, tokens, pattern)
    hi = right_bound(sa, tokens, pattern)
    k = len(pattern)
    return [tokens[i+k] for i in sa[lo:hi] if i + k < len(tokens)] # packs all tokens that match in a list and returns

def generate(tokens, sa, order, max_output):
    
    output = list(tokens[:order])
    if len(output) >= max_output:
        return output[:max_output]

    pattern = tuple(output[-order:])

    while len(output) < max_output:
        candidates = continuations(sa, tokens, pattern)
        if not candidates:
            break

        next_token = random.choice(candidates)
        output.append(next_token)
        pattern = tuple(output[-order:])

    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", type=int, default=2)
    parser.add_argument("-w", action="store_true")
    parser.add_argument("-s", type=int, default=None)
    parser.add_argument("-m", type=int, default=1000, help="maximum output length")
    parser.add_argument("inputfile")
    args = parser.parse_args()

    if args.s is not None:
        random.seed(args.s)

    mode = "words" if args.w else "chars"
    tokens = read_input(args.inputfile, mode)
    sa = build_sa(tokens)
    generated = generate(tokens, sa, args.o, args.m)

    if args.w:
        print(textwrap.fill(" ".join(generated), width=70))
    else:
        print("".join(generated))


if __name__ == "__main__":
    main()


