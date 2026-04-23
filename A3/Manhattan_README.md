# Manhattan Problem
This python script offers a solution to the Manhattan Tourist Problem using dynamic programming. 
It supports horizontal/vertical (HV) and horizontal/vertical/diagonal (HVD) edge weights, with optional traceback to reconstruct the optimal path. 
------------------------------

## Dependencies
- Python 3.x or higher
- No external libaries are used 

- Used standard libaries: 
    - arparse

## Usage

```
python annadhm_manhattan.py [-t] [-d] Manhattan-test*.in
```

| Flag | Description |
|------|-------------|
| `Manhattan-test*.in` | input file (required) |
| `-d` | Enable diagonal moves (HVD mode) |
| `-t` | Enable traceback — prints score and path |

### Output
    If the `-t` flag is enabled, the path is printed, otherwise only the score is printed to the screen.

### Examples
Example ouputs from the provided tests are also uploaded to GitHub: annadhm-test*.out

```
    # HV mode, score only
    python annadhm_manhattan.py Manhattan-testHV*.in

    *Example Output:
    for the input: 
    '''
        ############################################################
        # Test input 1 for the Manhattan tourist problem
        #
        # small example instance
        #

        # size (north-south dimension times west-east dimension)
        # 3 3
        # north-south streets
        1 6 2
        4 0 7
        # west-east streets
        3 3
        3 2
        5 7
    '''
    the following output is expected: 
    '''
        18
    '''

    # HVD mode, score only
    python annadhm_manhattan.py -d Manhattan-testHVD*.in

    # HV mode with traceback
    python annadhm_manhattan.py -t Manhattan-testHV*.in

    *Example Output:
    for the same input used above, the following output is expected:
    '''
        18
        ESES
    '''

    # HVD mode with traceback 
    python annadhm_manhattan.py -d -t Manhattan-testHVD*.in
```

## Algorithm Steps
1. Parse input
2. Build:
    - <down> matrix (vertcial edges)
    - <right> matrix (horizontal edges)
    -  optionally <diagonal> matrix (diagonal edges)
3. inititalize DP table
4. Fill DP table
5. Trace back path of -t flag is set

## Features
- South moves are preferred over East moves over Diagonal moves
- The ouput is printed as integer if its a whole number, otherwise it is rounded to 2 didgits after the comma

## Accepted Input Formats
### HV Format (no divider)
Plain text file where: 
- first the size is reported (north-south dimension times west-east dimension)
- next n rows define the South (down) edge weights 
    - shape: n*m
- next n+1 rows define the East (right) edge weights
    - shape: (n+1) * (m-1)

### HVD Format (#--- divider)
Three blocks seperated by lines starting with `#---``
- down matrix with size
- right matrix with size
- diagonal matrix with size

# Error Handling
- Wrong matrix dimensions are catched by an error message
- Non-parsable inputs throw a ValueError

