# The Manhattan Tourist Problem:
This program solves the Manhattan Tourist Problem using dynamic programming. It computes the maximum number of sights that can be visited when moving from the top-left corner to the bottom-right corner of a grid. 
    If the optional flag `-d` is provided, diagonal edges are also taken into account. 
    If the optional flag `-t` is provided, the program additionally outputs the corresponding path.


# Processing the Command Line Arguments
The program is executed via the command line:
    python kralina123-Manhattan.py [-d] [-t] inputfile

The input file is provided as a command line argument (excluding the script's name and options starting with -).
    `-d`: enables diagonal moves
    `-t`: prints the corresponding path as a string (using S, E, and D) in addition to the maximum weight


# Processing Input File
The input file is read line by line. All comments (lines starting with #) are ignored and empty lines are skipped.

The number of columns `m` is determined by the length of the first data row.
The number of rows `n` is obtained by counting the consecutive rows of the same length `m`, which correspond to the north-south matrix of size `(n-1) x m`.

Next, the following matrices are constructed:
    `north_south`: Vertical edge weights, size `(n-1) x m`
    `west_east`: Horizontal edge weights, size `n x (m-1)`

If the `-d` option is enabled, additionally
    `diag_moves`: Diagonal edge weights, size `(n-1) x (m-1)` 
Otherwise, it remains empty.

All values are converted to floats. Since the input may contain decimal numbers written with commas, commas are replaced by dots before conversion.


# DP-Matrix
A DP matrix A is constructed, where each entry stores the maximum number of sights that can be collected when reaching the corresponding position in the grip.

The first row and column are initialized, since only one path leads to these positions. The remaining entries are filled row by row. For each cell, the maximum is taken either from the path coming from above (A[i-1][j] + north_south[i-1][j]) or from the left (A[i][j-1] + west_east[i][j-1]).

If diagonal moves are enabled, the path from the upper-left cell (A[i-1][j-1] + diag_moves[i-1][j-1]) is also considered.


# Output Base Case
The value in the bottom-right cell of the matrix A stores the maximum number of sights than can possibly be visited and is printed with two decimal digits.


# Traceback
If the -t flag is used, the path is reconstructed by backtracking from the bottom-right corner. At each step, it is determined whether the current value was obtained from above, from the left, or (if enabled) from the diagonal.

To avoid floating-point issues, comparisons are performed by checking whether the absolute difference between the current cell and the values from which it could have been reached is smaller than a small threshold (1e-9).

The corresponding move (S, E, or D) is then added to the beginning of the path.
In case of equal values, moving south is preferred, followed by moving east.