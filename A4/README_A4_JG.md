### Note
This README-file has been written using Claude Code, as I was really happy with it, when i used it for Assignment 3. I made minor changes but kept most of the suggestions.


# Markov Text Generator

A Markov model-based text generator. The program reads a training text, builds a model of observed contexts and their continuations, and generates new text by randomly sampling from those continuations.

## Usage

```
python julia-gro-Markov.py [options] [inputfile]
```

If no input file is given, the program reads from standard input.

### Options

| Flag | Description |
|------|-------------|
| `-o k` | Use Markov order `k` (default: 3) |
| `-w` | Use word-based generation instead of character-based |
| `-s seed` | Initialize the random number generator with `seed` |

Options and filename can be given in any order.

### Examples

```
python julia-gro-Markov.py erlkoenig.txt
```
```
python julia-gro-Markov.py -o 5 erlkoenig.txt
```
```
python julia-gro-Markov.py -w -o 2 -s 42 erlkoenig.txt
```
```
echo "one fish two fish red fish blue fish" | python julia-gro-Markov.py -w -o 2 -s 1
```

## Modes

### Character-based (default)

The model context consists of `k` consecutive characters. The program starts with the first `k` characters of the input and repeatedly picks the next character randomly from all observed continuations of the current context.

### Word-based (`-w`)

The model context consists of `k` consecutive words (whitespace-separated). Punctuation is not removed, so `word`, `word.`, and `word,` are treated as different words. Output is wrapped at approximately 70 characters per line.

## Algorithm

1. Read the full input text
2. Build a dictionary mapping each context (tuple of `k` units) to a list of observed next units
3. Start generation with the first `k` units as the initial context
4. Repeatedly sample a random continuation, append it to the output, and shift the context one unit forward
5. Stop when no continuation exists for the current context, or after 2000 units

## Reproducibility

Using the same input, options, and seed (`-s`) will always produce the same output.

## Testing & Known Edge Cases

| Test | Expected | Result |
|------|----------|--------|
| Same input + same seed, run twice | Identical output | ✓ |
| `-o` larger than text length | Output is just the initial context | ✓ |
| `-w -o 1` on a long text | Hits 2000 word limit | ✓ |
| No seed, run twice | Different outputs | ✓ |
| `"aaaa"` with `-o 1` | Long string of `a` until limit | ✓ |

**Issues encountered:**

- **Infinite loops at low orders:** Order 1 and 2 create cycles in short texts. Fixed by capping generation at 2000 units.
- **German special characters (ä, ö, ü, ß):** Windows defaulted to a non-UTF-8 encoding. Fixed by opening files with `encoding="utf-8"`.
- **Trailing newline in character mode:** When piping input, the trailing `\n` was included as a character and could terminate generation early. Fixed by stripping trailing newlines with `rstrip`.
