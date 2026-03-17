import sys

filename = sys.argv[1]

print("Hello world!")

with open (filename) as f:
    data = f.read()
    print(data)