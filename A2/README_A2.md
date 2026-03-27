# Use case 
The program "HannahSophie08-Administration.py" reads a cost matrix of cities as input and computes the partitions of the cities. It either finds the partition solutions that lie within a given cost limit or finds the minimum cost partition. 

# Approach
The program performs a recursive branch-and-bound search.

# Input
Expected file format:
    Line 1: <number of cities> <cost limit>
    Line 2: <city label 1> <city label 2> ...
    Line 3+: cost matrix 

The input file can be given via the command line. 

The program can be run like this:

python HannahSophie08-Administration.py [-o] <input_file> [output_file]

Example:
 
python HannahSophie08-Administration.py -o Administration-test1.in test1_out


# Command line Parameters
- - '-o': optional, if given the cost is optimized instead of enumerating the solutions within the cost limit
- Input file: path to the cost matrix
- Output file: optional, write results here instead of stdout 

# Output
If no output file name is given the output is printed, otherwise it is written to the given file. 
- without '-o': cities that share one authority are written as pairs and the pairs are ordered alphabetically
- with -'o': cost of best partition 

# Version
Requires Python 3

# Example

  8 10                      
   B  E  G  I  K  L  P  S  
 B  - 10 10  2 10 10 10 10  
 E 10  -  2 10 10 10  1 10
 G 10  2  - 10  2  3  3  3
 I  2 10 10  -  4 10 10  2
 K 10 10  2  4  - 10 10  3
 L 10 10  3 10 10  -  2  2
 P 10  1  3 10 10  2  - 10
 S 10 10  3  2  3  2 10  -

For this input the output without '-o' is:

BI EG KS LP
BI EP GK LS
BI EP GL KS

and with '-o':

7

# Date
27.03.2026