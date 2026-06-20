# Use Case 

The program "HannahSophie08-Manhattan.py" reads a street network as input where the streets are valued by the number of sights along them. The goal is to find the maximum-weight path through the grid. 

# Approach

The porgram uses dynamic programming. For each grid position, it stores the best total weight of any path from the top-left corner to that position.

# Input 

The input can be given in either one of these formats:
1. Labeld sections using comment headers as:
- north-south
- west-east
- diag
2. Unlabeled blocks

# Command line Parameters

- d: optional, allows diagonal moves
- t: optional, prints the best path in addition to the best score
- o: optional, file that the output should be written to

# Output 

The result is by default printed to stdout, except when the -o flag is given, then the output is printed to the given file.
When -t is given, the program outputs the best score and best path, otherwise only the best score is written to the output.

# Run the program

python HannahSophie08-Manhattan.py -d -t <input_file> -o <output_file>

# Version

Requires Python 3

22.04.2026