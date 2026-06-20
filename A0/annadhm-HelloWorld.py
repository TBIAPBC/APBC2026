"""
    Script for Assignment 0. 

    To use you need to hand over an input file and output file over the command line. 
    
    Like "python3 annadhm-HelloWorld.py HelloWorld-test1.in > HelloWorld-test1.out"

    If no input file is given an Error message occurs and the program stops. 
    If no ouput file is given, the output will be printed on the terminal. 

    Example output can be found in the expected_output.txt file:
"""

import sys

if len(sys.argv) < 2:
    print("Error! No input file given ")
    exit()

file = sys.argv[1]

with open (file, "r") as f:
    content = f.read()

print("Hello World!")
print(content, end="")