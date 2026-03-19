# A1 - Word Count 

The Python script reads a text file (name given over the command line) and counts the total number of words and the number of unique words by default. 

Optionally it prints a sorted list of words and their frequencies and / or ignores case letters (The=the). 

# REQUIREMENTS
- Python 3.13 or hogher
- No external dependencies (only standatd library)

# USED LIBRARIES
- sys (standard library)
- re (standard library)

 # FEATURES
 - Counts all words in a text file.
 - Counts number of unique words.
 - Optionally ignores case ('-I' flag)
 - Optionally prints a list of words and their frequencies ('-l' flag): 
    - Sorted first by frequency second alphabetically. 
- Ignores all punctuation and special symbols (e.g., '.?!§%&^/()-_+')
    - separate Words 
-Provides error messages for missing files or invalid flags. 

# USAGE INSTRUCTIONS
Run the script from the command line via:
    'pthon annadhm-WordCount.py [options] WordCount-test*.in'
    ! Make sure you run the input file is in the same directory as the code file. 

[options]:
    -I: ignore case (converts all letters to lowercase)
    -l: Print word list with frequency
# INPUT METHODS
The script supports two input methods:

1. File argument:
    python annadhm-WordCount.py <input_file>
2. Standard input (stdin):
    python annadhm-WordCount.py < <input_file>

# EXAMPLES with Outputs:
Count total words and unique words:
    python annadhm-WordCount.py WordCount-test1.in
    
    Output example : 
    78 / 89

Ignore case:
    python annadhm-WordCount.py -I WordCount-test2.in 

    Output example:
    442 / 1104

List case: 
    python annadhm-WordCount.py -l WordCount-test2.in 
    
    Output example:
    the 56
    I 32
    and 30
    my 24
    ...

Print word frequency list, ignoring case:
    python annadhm-WordCount.py -I -l WordCount-test3.in 

    output example:
    und	55
    die	41
    er	25
    ...

# ERROR HANDLING
- Unknown flag: Prints error message and usage instructions. 
- Missing file: Prints error message and usage instructions. 
- File not found: Prints descriptive error. 

# TROUBLESHOOTING
- Make sure input file path is correct. 
- Use 'python3' instead of 'python' if Python 2 is installed. 
- Make sure file exist. 
- If using '<', make sure the file is not empty. 
