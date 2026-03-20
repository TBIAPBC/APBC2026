#!/bin/python3

import sys
import re

filename = None
print_list = False
case_insensitive = False

del (sys.argv[0])
for arg in sys.argv:
    if "-l" == arg:
        print_list = True
    elif "-I" == arg:
        case_insensitive = True
    else:
        filename = arg

if filename == None:
    file = sys.stdin
else:
    file = open(filename)

with file:
    hist = {}
    for line in file:
        words = re.split(r"[\W]", line)
        words = list(filter(lambda word: word != "", words))
        for word in words:
            if case_insensitive:
                word = word.lower()
            if word in hist:
                hist[word] += 1
            else:
                hist[word] = 1
    hist = dict(sorted(hist.items(), key=lambda item: (-item[1], item[0])))
    if print_list:
        for key, value in hist.items():
            print(f"{key}\t{value}")
    else:        
        unique_words = len(hist)  
        total_words = sum(hist.values())         
        print(f"{unique_words} / {total_words}")
