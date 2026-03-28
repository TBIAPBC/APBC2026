# WordCount

This program reads a text file and counts the total number of words and the number of different words.  
Optionally, it can print a list of all words sorted by frequency.


## Requirements

Python ≥ 3.13.11
The program only uses modules from the Python standard library (argparse, re, sys).

The input file must either be located in the current working directory or the full/relative path to the file must be provided.


## Arguments

| Argument  | Description |
|-----------|-------------|
| filename  | Input text file |
| -I        | Ignore case when counting words (convert uppercase to lowercase)  |
| -l        | Print a list of words sorted by frequency (descending). Words with equal frequency are sorted alphabetically |
| -out FILE | Write the output to a file instead of printing to the terminal |


## Example Usage

# For Test1
python AnesIms-WordCount.py WordCount-test1.in -out test1.out

# For Test2
python AnesIms-WordCount.py WordCount-test2.in -l -out test2.out

# For Test3
python AnesIms-WordCount.py WordCount-test3.in -l -I -out test3.out

# For STDIN
python AnesIms-WordCount.py < WordCount-test1.in