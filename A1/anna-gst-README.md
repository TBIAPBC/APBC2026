# A1 - Word Count
Last update: 19.03.26
Responsible Author: Anna Gsteu

## Description
This Python script reads a text file and counts the total number of words and the number of unique words. Optionally, it can ignore case and print a sorted list of words with their frequencies.

### Requirements:
- Python 3

### How to run:
Run the script from the command line and provide an input file as an argument:
```
python anna-gst-WordCount.py inputfile
```

### Options:
- `-I` — ignore case (e.g. "The" and "the" are counted as the same word)
- `-l` — print a sorted list of words and their frequencies

### Examples:
```
python anna-gst-WordCount.py inputfile
python anna-gst-WordCount.py -I inputfile
python anna-gst-WordCount.py -l inputfile
python anna-gst-WordCount.py -l -I inputfile
```

### Output files
You can save the output into a file using redirection:
```
python anna-gst-WordCount.py inputfile > outputfile
```