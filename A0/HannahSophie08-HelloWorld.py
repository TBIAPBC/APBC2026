''' Solution for exercise A0 in python 
Run with: python HannahSophie08-HelloWorld.py input_file (if the input file is in the same directionary,
otherwise give the file path)
Output with HelloWorld-test1.out: 
Hello World

That's all folks!
'''


import sys

print("Hello World\n")

filename = sys.argv[1]

with open(filename, "r") as f:
    content = f.read()

print(content)