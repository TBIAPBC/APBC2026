# Markov Text Generator

A Python tool that generates text using Markov chains. Train it on any text file and it will generate new text in a similar style by learning character or word-level patterns.

## Features

- **Character mode** (default): Generates text by predicting the next character based on preceding characters
- **Word mode** (`-w`): Generates text by predicting the next word based on preceding words
- **Configurable order**: Control the context length (how many preceding tokens influence predictions)
- **Reproducible output**: Use a seed value to generate the same text repeatedly

## Packages

Uses the random and argparse packages.

## Basic Usage
``` 
python the-other-thanos-markov.py input.txt
```
## Command-Line Options
```
-w, --words           Use word mode instead of character mode
-o, --order INT       Set the context length (default: 1)
-s, --seed INT        Set random seed for reproducible output
```

## Example
#### Use word mode with context length 2 and a seed
```
python the-other-thanos-markov.py text.txt -w -o 2 -s 42
```
## Structure

- Read input: The tool reads your text file and creates a text string 
- Build model: It creates a Markov chain by tokenizing the text string depending on the mode and records what tokens follow each k-length context
- Generate: Starting with the first k tokens, it randomly selects the next token from all possible continuations until reaching the end of the text

