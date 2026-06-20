import sys

filename = sys.argv[1]

print("Hello World!")

with open (filename) as f:
    print(f.read(), end="")