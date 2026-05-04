# A4 - Markov Text Generator 
This program generates new text from an input text a Markov model. 

# Description
The program reads a training text from an input file and builds a markov model of oder k. It generates new text by randomly choosing one of the continuations that actually occur in the input text.
In character mode, the model works with individual characters. 
In word mode, the model works with words.

# Usage
The program is executed via the command line:
python kralina123-Markov.py -o k [-w] [-s seed] inputfile
# Input arguments
    '-o k': Defines the order of the Markov model.
    '-w': Optional flag. If activated the model works word-based.
    '-s seed': Optional. If activated, the random number generator is initialized with the given seed (integer) for reproducible output.

# Processing Input File
The input text is internally stored as a list.
In character mode each character is one entry. Line breaks are treated as whitespace and tabs are ignored.
In word mode, the string is split at every whitespace. Each entry of the list is a word (possibly with special characters).
If the seed option is provided, the random number generator is initialized accordingly. 

# Markov Model
The first k entries of the input are the initial context. A suffix array is used to store the starting positions of all suffixes, sorted lexicographically.

The algorithm proceeds as follows:
1. All positions where the current context occurs are found with binary search (using bisect_left and bisect_right).
2. One occurance is selected randomly.
3. The character/word that follows the context from the selected suffix is appended to the output.
4. The context is updated to the last k elements of the current output text.

The steps 1-4 are repeated as long as continuation is possible (a following element to an occurence of the context exists). 

# Output
The generated list is joined into a string. In word mode elements are joined with whitespace and wrapped to approximately 70 characters per line. The resulting string is then printed to standard output.

# Error Handling 
If the Markov Order k is larger than the input length, an error is printed to standard error and the program terminated without producing output.
To avoid infinite loops, the generation process is limited to 1000 iterations.