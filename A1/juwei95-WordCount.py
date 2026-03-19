import sys
import re

filename = sys.argv[-1]

with open(filename) as f:
    lines = f.readlines()
    hist = {}
    for line in lines:
        words = re.split(r"[\W]", line)
        words = list(filter(lambda word: word != "", words))
        for word in words:
            if "-I" in sys.argv:
                word = word.lower()
            if word in hist:
                hist[word] += 1
            else:
                hist[word] = 1
    hist = dict(sorted(hist.items(), key=lambda item: (-item[1], item[0])))
    if "-l" in sys.argv:
        for key, value in hist.items():
            print(f"{key}\t{value}")
    else:        
        unique_words = len(hist)  
        total_words = sum(hist.values())         
        print(f"{unique_words} / {total_words}")