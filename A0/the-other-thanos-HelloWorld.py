import sys

def hello(filename):
    try:
        with open(filename) as f:
            print('Hello World!')
            file_content=f.read()
            print(file_content.rstrip())
    except:
        print(f"Error reading the file \"{filename}\", make sure the file exists and the name is correct.")
            
if len(sys.argv)<2: 
    sys.exit("No input file specified")
else:
    input_file=sys.argv[1]
       
hello(input_file)