import sys

with open(sys.argv[1]) as f:
	text = f.read()

print("Hello World!")
print(text, end="")