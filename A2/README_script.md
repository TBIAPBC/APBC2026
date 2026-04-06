#A2 Assignment, Administration
Python script which uses command-line tools to assign administration for an even numbered list of cities given a cost matrix. The file passed to the script was tested out for standard text files.

## Usage
Run the script from the terminal by providing a text file as the primary argument containing the key information. Use the -o flag for optimization if you want to only see the administrative partitioníng with the smallest bill.
If there are combinations which share the same minimum cost then all paths with the same cost will be displayed.

```bash
python BeatriceHN-Administration.py input.txt -o

