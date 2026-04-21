# A3 - Manhattan Tourist Problem
Last update: 21.04.26

Author: Anna Gsteu

## Description
This Python script solves the Manhattan Tourist Problem using dynamic programming. It reads a grid of street weights from an input file and finds the maximum-weight path from the top-left to the bottom-right corner. Works for both HV (horizontal/vertical) and HVD (with diagonals) input files.

## Approach
I used **dynamic programming** with a 2D matrix `dp`, where `dp[i][j]` stores the best path weight from start to the crossing `(i, j)`. Each cell is filled by looking at the possible previous cells (above, left, and diagonal if `-d`) and taking the max. The final answer is at the bottom-right corner.

For the `-t` flag, traceback walks backward from the end corner and at each step figures out which predecessor produced the current cell's value. Tie-breaking order is S > D > E, so the tourist prefers going south.

### Requirements:
- Python 3

### How to run:
```
python anna-gst-Manhattan.py inputfile
```

### Options:
- `-d` — enables diagonal mode (input file must contain a third matrix of diagonal weights)
- `-t` — additionally prints the best path as a string of E/S/D moves
- `-m` — prints the filled DP matrix (for debugging)

### Examples:
```
python anna-gst-Manhattan.py Manhattan-testHV1.in
python anna-gst-Manhattan.py Manhattan-testHV1.in -t
python anna-gst-Manhattan.py Manhattan-testHV1.in -t -m
python anna-gst-Manhattan.py Manhattan-testHVD2.in -d -t
```

### Example output (testHV1, with -t):
```
18
ESES
```

### Input format
The input file should contain 2 (HV) or 3 (HVD) matrices of edge weights. Comments (`#`) and blank lines are ignored. Block order: down, right, diagonal (if HVD). European-style decimal commas are accepted (idea from looking at @Ez3k4's A3).

### Error handling
The script checks for:
- missing or unreadable input file
- fewer than 2 matrices in the input
- missing diagonal matrix when `-d` is set
- matrix shapes not matching the grid geometry
