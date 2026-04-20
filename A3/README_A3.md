# A3: Manhattan Tourist Problem

## Overview

This project is an implementation of the Manhattan Tourist Problem, which asks for the longest path from the top-left corner to the bottom-right corner of a grid, where each move is restricted to South, East, and (optionally) Diagonal steps, and edge weights represent "scores" for each transition.

## Files

- **eweindorfer-Manhattan.py**: 
  The main Python script which reads input matrices (including optional diagonal moves), calculates the maximum scoring path using a dynamic programming approach, and can print both the computed score matrix and the resulting path.
- **README_A3.md**: 
  This file. Contains usage instructions, explanations, and background for the assignment.

## Input Format

The code expects an input file with the following format:

For an *m × n* grid:
- The first *m - 1* lines must contain *n* edge weights for all "down" (vertical) scores
- Followed by *m* lines containing *n - 1* "right" (horizontal) scores
- If diagonal moves are enabled, *m - 1* additional lines specifying *n - 1* diagonal scores are required

- All comments, empty lines, and invalid numbers are ignored

## Running the Code

1. **Prepare Input**:
    - Prepare a file with the grid edge weights according to the expected format.

2. **Run the script**:

    ```bash
    python eweindorfer-Manhattan.py <input-file> [-d] [-t] [-debug]
    ```
    - `<input-file>`: Path to the input file containing edge weights in the required format.
    - `-d`: Enable support for diagonal moves (i.e., allow path to follow South-East diagonals if the diagonal matrix is supplied in the input).
    - `-t`: Additionally prints the optimal path.
    - `-debug`: Enables debug output. Will print the parsed weight matrices and the score matrix for inspection.


3. **Output**:
    - The script prints the edge weights loaded from your file.
    - If `-t` is enabled, the optimal path (as a string of directions 'S', 'E', and optionally 'D') is printed.

## Code Features

- **Dynamic Programming Approach**: 
  The `calculate_score_matrix` function builds up the solution efficiently using previously computed sub-solutions.
- **Path Reconstruction**: 
  The `print_path` function reconstructs and prints the actual path taken to achieve the maximum score.
- **Input Validation**:
  The code checks input consistency (number of weights) and reports problems with colored output for clarity. I'm unsure if the color works on OSs other than Windows.
- **Customization**:
  Easily enable or disable diagonal moves by changing the `d` flag in the input parser.

## Functions

- `parse_numbers(line)`: Utility to parse integer weights from a line.
- `print_weights(down, right, diag)`: Prints out the parsed weight matrices.
- `calculate_score_matrix(down, right, diag, t, debug=False)`: Builds the score matrix and tracks the optimal direction at each step.
- `print_path(score_matrix)`: Reconstructs and prints the optimal path from the bottom right back to the start.

## Example

Suppose you have a grid with 3 rows and 4 columns. Your input file (`input.in`) might look like:

```
1 0 2 4
4 6 5 2

3 2 4
9 7 3
6 2 1
```
