# A2 - Administration of Atirasu
Last update: 07.04.26
Responsible Author: Anna Gsteu

## Description
This Python script partitions a set of cities into pairs and finds all combinations that stay within a given cost budget. It reads a cost matrix from an input file and uses branch and bound to avoid exploring paths that are already too expensive. With the `-o` flag, it finds the cheapest possible solution instead of listing all valid ones.

## Approach 
The taskl: pair up all cities, check if the total cost is within budget. Brute force would work for small inputs but gets slow fast (14 cities = 135,135 possible partitions).

So I used **branch and bound**, which is really just a recursive search (DFS) that stops early when the cost so far already exceeds the limit. The key trick to avoid duplicates: always pick the first unpaired city alphabetically and try pairing it with each remaining city. That way each partition is only found once, and the output is automatically in lexicographic order.

For the `-o` flag, the idea is the same but the bound gets tighter with every better solution we find. So the search gets faster as it goes.

### Requirements:
- Python 3

### How to run:
Run the script from the command line and provide an input file as an argument:
```
python anna-gst-Administration.py inputfile
```

### Options:
- `-o` — instead of listing all solutions, prints only the cost of the cheapest one

### Examples:
```
python anna-gst-Administration.py Administration-test1.in
python anna-gst-Administration.py -o Administration-test1.in
```

### Example output (test1, without -o):
```
BI EG KS LP
BI EP GK LS
BI EP GL KS
```

### Example output (test1, with -o):
```
7
```

### Output files
You can save the output into a file using redirection:
```
python anna-gst-Administration.py Administration-test1.in > output.txt
```

### Input format
The input file should look like this (no comments in the actual file):
```
8 10                     <- number of cities and cost limit
B  E  G  I  K  L  P  S  <- city names (alphabetically sorted)
- 10 10  2 10 10 10 10   <- symmetric cost matrix
10  -  2 10 10 10  1 10
...
```

### Error handling
The script checks for:
- missing or unreadable input file
- wrong number of header lines
- city count not matching the header
- matrix dimensions not matching
