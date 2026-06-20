# Task Description
APBC A2 - Administration

We must partition an even number of cities into pairs (2 cities per authority).
Each pair (x,y) contributes a cost read from a symmetric matrix.
Total cost must be <= given limit to be a valid solution.

# Input
File input format:

  num_cities cost_limit

  city_1 city_2 ... city_n

  n matrix rows with pair-cost values ('-' for diagonals)

# Output
Output is printed to commandline

Uniqueness of output (enumeration):

For each partition we print a canonical string:
- within each pair, print the two city names in sorted order
- then sort the pair-tokens lexicographically

# Run Script
Command format: python eweindorfer-Administration.py [-o] <input_file>

- Default mode: enumerate all partitions with total cost <= limit and print all solutions
- Optimization mode (-o): only find and print best possible score.

example command:
python eweindorfer-Administration.py -o Administration-test1.in
