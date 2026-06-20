import sys

print('Hello World!')

arg1 = sys.argv[1]

with open(arg1, 'r') as f:
    print(f.read())

