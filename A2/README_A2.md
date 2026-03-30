# Administration

This program solves the administration pairing problem by reading a cost matrix from an input file and generating valid pairings of capitals.



## Overview

The script reads an input file containing:

- the number of capitals and a cost limit
- the capital names
- a symmetric cost matrix

It then computes all valid pairings whose total cost does not exceed the given cost limit.

Additionally, the program supports an optimization mode via `-o`, which prints only the best score instead of all valid solutions.

### Additional Implementations

#### -s

An additional argument `-s` was added. When used together with `-o`, the program prints the best score and the corresponding best solution(s).
This makes it easier to directly see which solution(s) achieve the optimum.

When `-s` is used without `-o`, the program prints the default output, i.e all valid solutions. 

#### Parsing

Even though the input format was defined in the assignment, some checks were added, in case future inputs differ from the assignment input files.



## Requirements

Python 3.x 
The program only uses modules from the Python standard library (argparse, sys).

The input file must either be located in the current working directory or the full/relative path to the file must be provided.



## Arguments

| Argument | Description |
| --- | --- |
| `filename` | Optional input file. If no file is given, the program reads from standard input. |
| `-o` | Prints the score of the best solution. |
| `-s` | Use in combination with `-o`, to see the solution(s) with the best score. |
| `--out` | Defines the output file (`OUTPUT.out`). |



## Example Usage

### Default run

python AnesIms-Administration.py  Administration-test1.in

#### expected output default

```
BI EG KS LP
BI EP GK LS
BI EP GL KS
```

### Run with -o prints the best score

python AnesIms-Administration.py  Administration-test1.in -o

#### Expected output -o 

7


### Run with -o and --out ; The best score will be saved in .out file 

python AnesIms-Administration.py  Administration-test1.in -o --out best_cost_test1.out


### Run with -o -s and --out to save the best score and the corresponding best solution

python AnesIms-Administration.py  Administration-test1.in -o -s --out best_solution1.out

#### Expected output -o -s

```
7
BI EP GK LS
```

### Read from STDIN
python AnesIms-Administration.py < Administration-test1.in                             

#### Expected output STDIN <

```
BI EG KS LP
BI EP GK LS
BI EP GL KS
```