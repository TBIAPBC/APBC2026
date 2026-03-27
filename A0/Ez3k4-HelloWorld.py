#!/usr/bin/env python3

import sys

filename = sys.argv[1]

print("Hello World!")
with open(filename, "rt") as fh:
    for line in fh:
        line = line.rstrip("\n")
        print(line)
