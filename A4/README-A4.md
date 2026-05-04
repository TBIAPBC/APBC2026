# README for annadhm-Markov.py 
This python skript generates new text from an input text using a Markov model. The program reads a text, finds repeated contexts, and randomly selects continuations observed in the input. 

## Approach
A Markov model of order k is build as a dictionary:
- **key**: context of k conecutive characters (or words)
- **value**: list of all observed continuations in the input

Text generation:
1. Starts with the first k units of the input as initial context
2. Looks up current context in the dictionary
3. Randomly selcets one continuation from the list
4. Shifts context one uni to the right
5. Repeat until no valid continuation exists or max output length (5 x input length) is reached 

## Usage
''' python annadhm-Makov.py [options] [inputfile] '''

If no input file is given, the program reads from the standard input. Only one input file is allowed per run. 

## Dependencies 
Requires:
 - Python 3.x or higher

Only standard python libaries are used:
- argparse
- random
- sys
- textwrap

## Options
-o k        : Markov order k (default: 1)
-w          : Word-based generation instead of character-based
-s seed     : Seed for the random number generator (reproducibility)
<inputfile> : reads input text from this file (optional)

### Modes
**Character-based (default):**
    The model context consists of k consecutive characters. 
    The generated text is built character by character. 
    Lower values of k produce more random-looking text, while higher values copy longer fragments from the input. 

**Word-based (-w):**
    The model context consists of k consecutive words. 
    Words are defined as whitespace-seperated tokens. 
    Punctuation is not removed, 'Hello' and 'Hello.' are treatened as different words. 
    The output is always composed of words that appear in the input. 

### Example input and output
input.txt contains "one fish two fish red fish blue fish" to demonstrate execute commands and output examples. 

***Input over input file***
    '''python annadhm-Markov.py input.txt'''

Output: 
    '''
    one fish fish fish blue fish fish blued fish twone fish re fish fish
    fish red blue re fish fish fish fish blue fish fish twone twone blued
    blue blue fish fish fish fish fish fish b
    '''
***-o Flag***
    '''python annadhm-Markov.py -o 3 input.txt'''
Output:
    '''
    one fish blue fish two fish red fish red fish red fish blue fish red
    fish two fish blue fish two fish blue fish blue fish red fish red fish
    two fish blue fish red fish blue fish re
    '''
***-o and -w Flag***
    '''python annadhm-Markov.py -o 3 -w input.txt'''
Output:
    '''
    one fish two fish red fish blue fish
    '''
***-o, -w and -s Flag***
    '''python annadhm-Markov.py -o 3 -w -s 4 input.txt'''
Output:
    '''
    one fish two fish red fish blue fish
    '''
***Input over standard input***
    '''echo "one fish two fish red fish blue fish" | python annadhm-Markov.py [options]'''
    ''' cat input.txt | python annadhm-Markov.py [options]'''
Output:
    '''
    oned re red red fish fish blue blued two fish blue fish blued two fish
    two blued re fish fish re blue fish red fish twone fish red fish fish
    re re fish re blue fish blue blue fish
    '''

- Note if -w or / and -s flag is used without setting the -o flag, standard -o of 1 is used. 


## Erro handling
- error messages and warnings are printed to stderr. 
- The following errors are handled:
    - empty input file
    - use of zero or a negative number for Markov order k
    - to short input text for the chosen Markov order k

## Notes
- Output is wrapped at around 70 characters per line. 
- Same input, options, and seed always produce the same output. 
- For short or cyclic inputs, output length is capped at 5* the input length to avoid infifnited loops (like 'banana' would lead to)

#### Date: 04.05.2026
