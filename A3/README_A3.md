# Manhattan Tourist Problem

This program solves the Manhattan Tourist Problem by dynamic programming.  
It reads an input file containing street weights and computes the maximum path weight from the top-left to the bottom-right corner of the grid.

The program supports both:

- horizontal/vertical input files (HV)
- horizontal/vertical/diagonal input files (HVD)



## Overview

The script reads an input file containing edge weights for a Manhattan-like grid.

For HV input, the program parses:

- north-south streets (`down`)
- west-east streets (`right`)

For HVD input, the program additionally parses:

- diagonal streets (`diag`)

It then computes the maximum path weight using dynamic programming.

If `-t` is used, the program also prints the corresponding best path.

### Additional Implementations

#### -d

The argument `-d` enables support for input files that also contain diagonal edge weights.  
Without `-d`, the program processes standard HV input.

#### -t

The argument `-t` prints both:

- the maximum path weight
- the corresponding best path

For HV input, the traceback consists of:

- `E` for east
- `S` for south

For HVD input, the traceback may additionally contain:

- `D` for diagonal

If several optimal paths exist, south is preferred in tie situations.

#### Parsing

Even though the input format was defined in the assignment, additional checks were implemented:

- comments are ignored for HV parsing
- empty lines are ignored
- decimal numbers are supported
- invalid dimensions are detected
- non-numeric values are detected
- HVD matrices are checked for rectangular shape and matching dimensions

#### Output formatting

If the result is an integer, it is printed as an integer.  
If the result is a floating point number, it is printed with two decimal places.


## Requirements

Python 3.x  
The program only uses modules from the Python standard library (`argparse`, `sys`).

The input file must either be located in the current working directory or the full/relative path to the file must be provided.



## Arguments

| Argument | Description |
| --- | --- |
| `filename` | Optional input file. If no file is given, the program reads from standard input. |
| `-d` | Additionally process input files with diagonals. |
| `-t` | Prints the weight of the maximum path and the corresponding best path. |
| `--out` | Defines the output file (`OUTPUT.out`). |



## Example Usage

### Default run with HV input
```
python AnesIms-Manhattan.py Manhattan-testHV1.in
```

#### Expected output default run HV
```
18
```

### Run with -t on HV input
```
python AnesIms-Manhattan.py Manhattan-testHV2.in -t
```

#### Expected output HV -t
```
104
ESEEESSSSEESSEE
```

### Run with HVD input
```
python AnesIms-Manhattan.py Manhattan-testHVD1.in -d
```

#### Expected output HVD -d
```
58.20
```

### Run with HVD input and traceback
```
python AnesIms-Manhattan.py Manhattan-testHVD1.in -d -t
```

#### Expected output -d -t
```
58.20
EDDEDSSDDDD
```

### Read from STDIN
```
python AnesIms-Manhattan.py < Manhattan-testHV1.in
```

#### Expected output STDIN
```
18
```

### Save output to file
```
python AnesIms-Manhattan.py Manhattan-testHV1.in --out result.out
```
