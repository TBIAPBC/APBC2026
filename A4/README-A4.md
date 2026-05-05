# Markov Text Generator

This program generates new text from an input text using a Markov model.  
It reads a training text, builds a model from observed contexts and continuations and then randomly generates new text based on this model.

The program supports both:

- character-based text generation
- word-based text generation



## Overview

The script reads an input text from a file or from standard input.

For character-based generation, the program uses:

- character contexts of length `k`
- observed following characters as possible continuations

For word-based generation, the program uses:

- word contexts of length `k`
- observed following words as possible continuations

It then generates text by repeatedly choosing one possible continuation at random.

If `-s` is used, the random number generator is initialized with a seed.  
This makes the generated output reproducible.



### Additional Implementations

#### -o

The argument `-o` defines the order `k` of the Markov model.

For character-based generation, `k` is the number of previous characters used as context.  
For word-based generation, `k` is the number of previous words used as context.

A higher order usually makes the output more similar to the input text, while a lower order usually produces more random-looking text.

#### -w

The argument `-w` enables word-based generation.

Without `-w`, the program uses character-based generation by default.

In word mode, words are separated by whitespace.  
Punctuation is not removed, so words such as `word`, `word.`, and `word,` may be treated as different words.

#### -s

The argument `-s` initializes the random number generator with a seed.

This is useful for testing and debugging, because the same input, the same Markov order, and the same seed produce the same output.

#### Input handling

The program accepts an optional input file.

If no input file is given, the program reads the training text from standard input.

Line breaks and repeated whitespace are treated as whitespace.  
The input text is internally normalized so that multiple whitespace characters are replaced by single spaces.

#### Error handling

Additional checks were implemented:

- the Markov order must be positive
- the input text must not be empty
- in character mode, the Markov order must be smaller than the number of characters in the input
- in word mode, the Markov order must be smaller than the number of words in the input

Error messages are printed to standard error.

#### Output formatting

The output contains only the generated text.

In word-based mode, generated words are joined by single spaces.



## Requirements

Python 3.x  
The program only uses modules from the Python standard library (`argparse`, `sys`, `random`).

The input file must either be located in the current working directory or the full/relative path to the file must be provided.



## Arguments

| Argument | Description |
| --- | --- |
| `filename` | Optional input file. If no file is given, the program reads from standard input. |
| `-o k` | Uses Markov order `k`. |
| `-w` | Uses word-based generation instead of character-based generation. |
| `-s seed` | Initializes the random number generator with `seed`. |



## Example Usage

### Default run with character-based generation
```
python AnesIms-Markov.py -o 4 glocke.txt
```

#### Example output default run character mode
```
Das ist die Himme Doch die heulend. Von der Stürmt in süßes Hausfrau, Die frommern Erblühen Meisten Glanzen Soll die losgelassen schwarzen finder Bande! ...
```

### Run with word-based generation
```
python AnesIms-Markov.py -o 1 -w sonnet18.txt
```

#### Example output word mode
```
Shall I compare thee to a summer’s day? Thou art more lovely and more lovely and more temperate: Rough winds do shake the eye of heaven shines, And often is his shade, When in eternal lines to thee.
```

### Run with word-based generation and seed
```
python AnesIms-Markov.py -o 1 -w -s 42 sonnet18.txt
```

#### Expected output word mode with seed
```
Shall I compare thee to a summer’s day? Thou art more lovely and more lovely and more temperate: Rough winds do shake the eye of heaven shines, And often is his shade, When in eternal lines to thee.
```

### Run with German text
```
python AnesIms-Markov.py -o 2 -w -s 42 erlkoenig.txt
```

#### Expected output German word mode
```
Wer reitet so spät durch Nacht und Wind? Es ist der Vater mit seinem Kind. Er hat den Knaben wohl in dem Arm, Er faßt ihn sicher, er hält ihn warm. Mein Sohn, was birgst du so bang dein Gesicht? - Siehst Vater, du den Erlkönig nicht! Den Erlenkönig mit Kron’ und Schweif? - Mein Sohn, was birgst du so bang dein Gesicht? ...
```

### Read from STDIN
```
python AnesIms-Markov.py < sonnet18.txt -o 1 -w -s 42
```

#### Expected output STDIN
```
Shall I compare thee to a summer’s day? Thou art more lovely and more lovely and more temperate: Rough winds do shake the eye of heaven shines, And often is his shade, When in eternal lines to thee.
```