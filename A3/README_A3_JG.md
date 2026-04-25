### Note
This README-file has been written using Claude.ai, as I wanted to test, how well it works. I really enjoy its structure, so I decided on keeping most of the suggestions. 


# Manhattan Tourist Problem

A dynamic programming solution to the Manhattan Tourist Problem. The program finds the maximum-weight path from the top-left to the bottom-right corner of a grid, where the tourist can only move east, south, or optionally diagonally.

## Usage

```
python julia-gro_manhattan.py [options] <input_file>
```

### Options

| Flag | Description |
|------|-------------|
| `-t` | Print the best path in addition to the score (e.g. `ESES`) |
| `-d` | Process input files that also contain diagonal edge weights (HVD mode) |

Flags and filename can be given in any order.

### Examples

```
python julia-gro_manhattan.py Manhattan-testHV1.in
```
```
python julia-gro_manhattan.py -t Manhattan-testHV1.in
```
```
python julia-gro_manhattan.py -d Manhattan-testHVD1.in
```
```
python julia-gro_manhattan.py -t -d Manhattan-testHVD1.in
```

## Input File Format

The input file contains edge weights for the grid. Lines starting with `#` are treated as comments and ignored. Empty lines are also ignored.

### HV Mode (horizontal/vertical only)

The file contains two blocks of numbers:
1. **North-south streets** — `(N-1) x M` matrix of vertical edge weights
2. **West-east streets** — `N x (M-1)` matrix of horizontal edge weights

Example for a 3x3 grid:
```
# north-south streets
1 6 2
4 0 7
# west-east streets
3 3
3 2
5 7
```

### HVD Mode (horizontal/vertical/diagonal)

Same as HV, with an additional third block:

3. **Diagonal edges** — `(N-1) x (M-1)` matrix of diagonal edge weights

## Output

The program prints the maximum path weight to STDOUT. If `-t` is given, it also prints the path as a sequence of moves:
- `E` — move east
- `S` — move south
- `D` — move diagonally (only in HVD mode)

If multiple maximum paths exist, the program prefers moving south over east.

### Example output

```
18
ESES
```

## Algorithm

The program uses a 2D dynamic programming table where each cell stores the best score reachable from the start. The table is filled row by row, left to right. The optimal path is recovered by tracing back from the end corner to the start.