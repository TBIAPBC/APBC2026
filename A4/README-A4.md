# Markov Model Text Generator (A4 Assignment)

This repository contains a Python program for text generation using a Markov model of configurable order, as required for assignment A4.

## Features

- Supports both character-based and word-based Markov models.
- Case-insensitive option for input processing.
- Dynamic (animated) printing of generated text.
- Seedable random generation for reproducibility.
- Configurable maximum length for generated sequences.

## Usage

### Command-Line Arguments

| Argument                    | Description                                                         | Required |
|-----------------------------|---------------------------------------------------------------------|----------|
| `filename`                  | Input file containing source text                                   | Yes      |
| `-o k`                      | Markov order (integer); number of previous tokens used as context   | Yes      |
| `-s seed`                   | Seed for random number generator (string)                           | No       |
| `-w`                        | Use word-based instead of character-based processing                | No       |
| `-i`                        | Ignore case (make all input lowercase)                              | No       |
| `-d`                        | Enable dynamic printing (printing as generation progresses)         | No       |
| `-max n`                    | Limit output to at most `n` tokens                                  | No       |

### Example Commands

Generate 200 characters based on character 4-grams:
```
python eweindorfer-A4.py myfile.txt -o 4 -max 200
```

Generate 50 words based on word 2-grams, with case-insensitivity and animated output:
```
python eweindorfer-A4.py myfile.txt -o 2 -w -i -d -max 50
```

## Notes

- Input files should be plain text.
- In character-based mode, punctuation is removed and line breaks are replaced by spaces.
- In word-based mode, words are split at whitespace.

## Files

- `eweindorfer-A4.py` — main program file.
- `README-A4.md` — this documentation.

## Implementation

The implementation uses tuples to represent the context (the sequence of previous tokens) and a dictionary to map each context tuple to possible next tokens, efficiently storing and accessing the Markov model's state transitions.

## Dependencies

This project requires Python 3.6 or higher. All dependencies are part of the Python standard library; no external packages are needed.

- `argparse`
- `random`
- `string`
- `time`
