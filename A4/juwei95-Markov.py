import argparse
import sys
import random


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog='juwei95-Markov.py', description='Generates random text based on training data')
    parser.add_argument('-o', '--order', action='store',      metavar='k', default=1, type=int, help='use Markov order k')
    parser.add_argument('-w', '--words', action='store_true',                 help='use word-based generation instead of character-based generation')
    parser.add_argument('-s', '--seed',  action='store',      metavar='seed', default=0, help='initialize the random number generator with seed')
    parser.add_argument('filename',      action='store',      nargs='?',      help='input file name containing training text - if omitted, input is read from stdin')
    args = parser.parse_args()
    if args.order <= 0:
        print(f"Invalid order of {args.order}, order must be > 0!", file=sys.stderr)
        exit(-1)
    return args

def parse_file(args: argparse.Namespace):
    if args.filename:
        infile = open(args.filename)
    else:
        infile = sys.stdin
    tokens = []
    for line in infile:
        if args.words:
            tokens.extend(filter(lambda word: word != "", line.split()))
        else:
            tokens.extend(list(line))
    if args.filename:
        infile.close()
    return tokens

def build_continuation_map(tokens: list[str], args: argparse.Namespace) -> dict[tuple[str], list[str]]:
    continuation_map: dict[tuple[str], list[str]] = {}
    for pos in range(len(tokens) - args.order):
        key = tuple(tokens[pos:pos + args.order])
        value = tokens[pos + args.order]
        if key in continuation_map:
            continuation_map[key].append(value)
        else:
            continuation_map[key] = [value]
    return continuation_map

def print_output_token(token: str, args: argparse.Namespace):
    print(token, end=" " if args.words else "")

def generate_text(continuation_map: dict[tuple[str], list[str]], tokens: list[str], args: argparse.Namespace):
    random.seed(args.seed)
    context = tokens[:args.order]
    for token in tokens[:args.order]:
        yield token
    while tuple(context) in continuation_map:
        continuations = continuation_map[tuple(context)]
        next_token = continuations[random.randrange(len(continuations))]
        context.pop(0)
        context.append(next_token)
        yield next_token

def main():
    args = parse_args()
    tokens = parse_file(args)
    continuation_map = build_continuation_map(tokens, args)
    try:
        for token in generate_text(continuation_map, tokens, args):
            print_output_token(token, args)
    except KeyboardInterrupt:
        pass
    print()

if __name__ == "__main__":
    main()
