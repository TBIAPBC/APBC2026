# Ez3k4-Markov.py

`Ez3k4-Markov.py` is a small Markov text generator.

It reads a training text, builds a suffix-array-based lookup table,
and then generates new text by repeatedly choosing a random valid
continuation for the current context.

## Usage

```bash
python3 Ez3k4-Markov.py -o K [-w] [-s SEED] [-m MAX_OUTPUT] inputfile
```

The script currently expects one input file.

## Options

- `-o K` sets the Markov order, that is, the number of characters or
	words used as context.
- `-w` switches from character mode to word mode.
- `-s SEED` sets the random seed so runs become reproducible.
- `-m MAX_OUTPUT` sets the maximum number of generated tokens. In
	character mode, this is the maximum number of characters. In word
	mode, this is the maximum number of words.

## Examples

Character mode with order 3:

```bash
python3 Ez3k4-Markov.py -o 3 fish.txt
```

Word mode with order 2 and a fixed seed:

```bash
python3 Ez3k4-Markov.py -o 2 -w -s 42 -m 200 fish.txt
```

## Notes

- The program uses the first `k` characters or words of the input as
	the initial context.
- It stops when no continuation is possible or when the maximum output
	length is reached.
- In word mode, the output is wrapped to about 70 characters per line
	for readability.
