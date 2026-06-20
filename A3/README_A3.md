## A3 Manhattan Tour

A Python script which solves the Manhattan tour problem. This program accepts input files which have descriptors denoted by [#] (e.g.: # North-West) and without descriptors for the input matrix.

The algorithm is able to solve basic north-south and west-east matrices as well as diagonal matrices which represent the streets of the Manhattan problem.

### Usage

    python BeatriceHN-Manhatten-test.py input_file

There are additional flags that can be used to change the output or input instructions:

| Flag  | Function                                                        |
|-------|-----------------------------------------------------------------|
| -d    | Use -d if the input file contains a matrix for diagonal weights | 
| -t    | Use -t if you want the best path to be printed to terminal      |

The basic output without the flags will be the total weight of the best path.

### Technical Details
If two paths (+d) have equal weights, then a rank system is used to decide which path to take. The rank system South > East > Diagonal is used to prioritize moving down towards the southeast sink.

### File with descriptors
The following keywords are identified in a file with descriptors:
[down, north-south, n-s, vertical, v, right, west-east, w-e, horizontal, h, diag, diagonal, d]