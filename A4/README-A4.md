# Markov Text Generator

This program generates text from an input text using a Markov model.

It supports two modes:

- character-based generation
- word-based generation

The Markov order `k` is configurable from the command line.

For the input every following k szbstring or word gets added which autmoatically makes them appear more often so it is equal to the probabilites, when reconstructing because the chances of selecting it are higher when they are more often in the list.

After analyzing the input and creating the list for possible next chars, words the dict gets used to recreate the output until eventually a char or word is choosen without next word or indefintely, therefore i also made a comment where to change the code to make a finite version of the code. 

Depending on the mode the word or char version of the code runs also with different k lenght. 


## Files

- `najak04-markov.py` — the Python program


## Requirements

- Python 3

## Usage

python3 najak04-markov.py -o k [options] [inputfile]
