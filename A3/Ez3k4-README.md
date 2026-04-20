# Manhattan Tourist Solver

## Usage

```bash
python Ez3k4-Manhattan.py [options] <input_file>
```

### Options

- `-d` Enable diagonal moves. Expects diagonal weights in the input file.
- `-t` Print the optimal path in addition to the maximum score.

### Examples

```bash
python Ez3k4-Manhattan.py Manhattan-testHV1.in
```

```bash
python Ez3k4-Manhattan.py -d -t Manhattan-testHVD1.in
```

## Description

This program solves the Manhattan Tourist Problem using dynamic programming.

Given a grid of edge weights, it computes:

- the maximum-weight path from the top-left corner to the bottom-right corner
- optionally, the path taken

### Allowed moves

- `E` East, right
- `S` South, down
- `D` Diagonal, only with `-d`

If multiple optimal paths exist, the program prefers moving South (`S`).

## Input Format

The input file defines edge weights of a grid.

### General rules

- Lines starting with `#` are comments and are ignored
- Empty lines are ignored
- Numbers can be integers like `5`
- Numbers can be decimals with `.` or `,` like `3.14` or `2,5`
- At most 2 digits are allowed after the decimal separator

### HV Input without diagonals

Example:

```text
# north-south streets (down)
1 6 2
4 0 7

# west-east streets (right)
3 3
3 2
5 7
```

Down matrix size: `(n-1) x m`

Right matrix size: `n x (m-1)`

### HVD Input with diagonals

Use `-d` for input files that also contain diagonal weights.

Example:

```text
#G_down:
0.60 0.65 0.91
...

#---
#G_right:
0.76 0.41
...

#---
#G_diag:
6.74 7.03
...
```

Down matrix: `(n-1) x m`

Right matrix: `n x (m-1)`

Diagonal matrix: `(n-1) x (m-1)`

## Output

The program prints the maximum path weight.

If `-t` is used, it also prints the optimal path.

### Path symbols

- `E` East
- `S` South
- `D` Diagonal

## Implementation Notes

- Uses dynamic programming to compute optimal scores
- Uses traceback to reconstruct the optimal path
- Floating-point arithmetic may introduce minor rounding artifacts in internal matrices