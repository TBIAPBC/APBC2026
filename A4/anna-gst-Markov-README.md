# A4 - Markov Text Generator
Last update: 03.05.26

Author: Anna Gsteu

## Description
This Python script generates new text from a training text using a Markov model. It reads an input text either from a file or from standard input and then creates new text based on character or word contexts found in the original text.

The program supports both character-based generation and word-based generation. The Markov order `k` can be set with the `-o` flag. A random seed can also be used to make the output reproducible.

## Approach
I used a dictionary-based Markov model. Each context of length `k` is stored as a key in the dictionary, and the possible next characters or words are stored in a list as the value.

In character mode, the context is a string of `k` characters.  
In word mode, the context is a tuple of `k` words, because lists cannot be used as dictionary keys.

The generated text starts with the first `k` characters or words of the input. Then the program repeatedly looks up the current context in the dictionary and randomly chooses one of the possible next characters or words. The context is updated after each step.

During testing I noticed that some inputs can generate text for a very long time, so I added the `-l` (length) flag as a limit. This helps avoid cases where the program looks like it is stuck.

Additionally, I added a `-i` (ignore cases) flag as discussed during the lecture, that allows users to run in a case insensitive mode.

For character mode I also changed the output from direct string addition to a list with `append()`. Before, I used `result += next_item`, but this copies the string again and again for longer outputs. With a list, the characters are collected first and joined at the end.

### Requirements:
- Python 3

### How to run:
'''
python anna-gst-Markov.py [options] [inputfile]
'''

If an input file is given, the program reads from the file.  
If no input file is given, the program reads from standard input.

### Options:
- `-o k` — sets the Markov order `k` (default = 1)
- `-w` — switches to word-based generation
- `-s seed` — sets the random seed for reproducible output
- `-i` — ignores upper/lowercase by converting the input text to lowercase
- `-l` — sets the maximum output length to avoid very long generation

### Examples:
'''
python anna-gst-Markov.py erlkoenig.txt
python anna-gst-Markov.py -o 3 erlkoenig.txt
python anna-gst-Markov.py -o 3 -s 7 erlkoenig.txt
python anna-gst-Markov.py -w -o 2 erlkoenig.txt
python anna-gst-Markov.py -w -o 2 -s 7 erlkoenig.txt
python anna-gst-Markov.py -o 2 -s 7 -l 200 erlkoenig.txt
python anna-gst-Markov.py -o 2 -i erlkoenig.txt
'''

the program generates text based on the word pairs found in the input. Since randomness is involved, the exact output can differ unless the same seed is used.

### Input format
The input is ordinary text. Empty lines and line breaks are treated as whitespace. In character mode, line breaks are replaced with spaces. In word mode, the text is split into words using whitespace.

Punctuation is not removed. This means that words like `word`, `word,` and `word.` are treated as different words in word mode.

### Error handling
The script checks for:
- missing or unreadable input file
- empty input text
- Markov order smaller than 1
- input text that is too short for the chosen Markov order
- maximum output length smaller than 1
- maximum output length smaller than the chosen Markov order