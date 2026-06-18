# A2 - Administration

Generates valid pairings of capitals under a cost limit using depth-first search with optional branch-and-bound optimization.

## Usage

```bash
python juwei95-Administration.py < Administration-test1.in
python juwei95-Administration.py -o < Administration-test1.in
```

## Input

```
8 10
 B  E  G  I  K  L  P  S
 - 10 10  2 10 10 10 10
10  -  2 10 10 10  1 10
10  2  - 10  2  3  3  3
 2 10 10  -  4 10 10  2
10 10  2  4  - 10 10  3
10 10  3 10 10  -  2  2
10  1  3 10 10  2  - 10
10 10  3  2  3  2 10  -
```

## Output

* Default: all valid pairings within the cost limit
* `-o`: minimum total cost only

## Details

* Depth-first search over pairings
* Branch-and-bound pruning via cost heuristic
* Implemented in python using only standard library modules.
* Tested using python 3.12.12 on Ubuntu 24.04.3 LTS under WSL.