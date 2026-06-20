"""
    Script for Assignment 1 - Word Count. 

    This script reads in a text file (name given over the command line) and counts the total number of words 
    and number of different words by default. 

    Two flag options are available: 
        - I : (Ignore) Upper case letters are ignored over converting all upper case letters to lover case letters
        - l : (list) prints a list of words instead of only counts: 
                - prints one word per line with its frequency. 
                - words are sorted alphabetically in case of equal frequencies. 
    
    To use, hand over the input and (optional) ouput file over the command line, like:
        " python annadhm-WordCount.py < WordCount-test*.in > WordCount-test*.txt" 
    
    If no input file is given an error statement occurs. 
    If no output file is given, the output is printed to the terminal. 
    
    Example terminal commands:
        - annadhm-WordCount.py < WordCount-test*.py | input is also possible without using "<"
        - annadhm-WordCount.py -I WordCount-test*.py
        - annadhm-WordCount.py -l -I dateiname
    
    Example outputs and additional information is provided in the README-WC.md file.
               
"""

import sys
import re

def main():

    # === Parse command-line arguments ===
    ignore_case = False
    list_words = False
    file = None

    allowed_flags = {"-I", "-l"}
    
    
    flags = sys.argv[1:]
    for flag in flags:
        if flag in allowed_flags:
            if flag == "-I":
                ignore_case = True
            elif flag == "-l":
                list_words = True
        elif flag.startswith("-"):
            print(f"Error: Unknown flag '{flag}'")
            print("try: '-I' or '-l' ")
            sys.exit(1)
        else:
            file = flag

    # === Read input file === 
    if not file and sys.stdin.isatty():
        print("Error: No input file or sdtin provided.")
        print("Try: python annadhm-Wordcount < WordCount-test*.in || OR || python annadhm-Wordcount WordCount-test*.in ")
        sys.exit(1)

    if file: 
        try:
            with open (file, 'r') as f:
                content = f.read()
        except FileNotFoundError:
            print(f"File {file} not found.")
            sys.exit(1)
    else:
        content = sys.stdin.read()

    # === convert to lower case letters if -l is enabled ===
    if ignore_case:
        content = content.lower()
    
    # split into words 
    words = [w for w in re.split(r'[^A-Za-z0-9ÄäÜüÖöß]+', content) if w]
    total_words = len(words)

    # count words over dictionary
    word_counts = {}
    for word in words:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1
    
    unique_words = len(word_counts)

    # === Ouput ===
    if list_words:
        # sorted first by frequency (descending) then alphabetically
        sorted_words = sorted(word_counts.items(), key=lambda x: (-x[1], x [0]))
        for word, count in sorted_words:
            print(f"{word} {count}")
    else:
        print(f"{unique_words} / {total_words}")
       


if __name__ == "__main__":
    main()