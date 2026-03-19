import sys

def hello(filename):
    with open(filename) as f:
        print('Hello World!')
        file_content=f.read()
        print(file_content.rstrip())
        
if len(sys.argv)<2: 
    sys.exit("No input file specified")
else:
    input_file=sys.argv[1]
       
hello(input_file)