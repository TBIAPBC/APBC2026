import sys


print("Hello World!")
filename = sys.argv[1]


with open(filename, "r") as f:
    text = f.read()

print(text)