# A2 - ADMINISTRATION

This python script reads a text file (name given over the command line) and solves a pairimng problem between cities using Branch and Bound algorithm. 
Provided with a set of citites and cost matrix, the programm generates all valid matchings (pairs of cities), whose total cost does not exceed a specific cost limit. 

The program operates in two modes:
- Enumeration mode (default): prints all valid pairings within the cost limit.
- Optimization mode: prints only the minimum possible total cost (int). 

## REQUREMENTS
- python 3
- No external dependencies (only standard library)

## USED LIBARIES
- sys (standard library)

## USAGE INSTRUCTIONS
```python annadhm-Administration.py <inputfile.in>```

Prints all valid pairings with total cost ≤ cost limit.

```python annadhm-Administration.py -o <inputfile.in>```

Optimization mode, the programm prints teh minimum total cost only. 

## INPUT METHODS

Provide input in file over the terminal. Use the command: 
python annadhm-Administration.py <inputfile.in>

Note: do not use "<" 

### Input Format
The input file must follow this structure:
<n> <cost_limit>
<city1> ... <cityn>
<cost row 1>
...
<cost row n>

- n:  number of cities.
- cost_limit:  maximum allowed total cost.
- list of city names.
-  n lines contain the cost matrix.
- "-" represents an unavailable connection.

Example:
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

## EXAMPLES WITH OUPUTS
python annadhm-Administration.py Administration-test1.in
    prints output to terminal: 
        
        BI EG KS LP
        BI EP GK LS
        BI EP GL KS

python annadhm-Administration.py Administration-test1.in > annadhm-Administration-test1.out
    prints output into output file
python annadhm-Administration.py Administration-test2.in > annadhm-Administration-test2.out
    prints output into output file

### Use of the flag -o:
python annadhm-Adminstration.py -o  Administration-test1.in
    Output: 7
python annadhm-Adminstration.py -o  Administration-test2.in
    Output: 9

## ERROR HANDLING
- Unknown flag: Prints error message and usage instructions.

## TROUBLE SHOOTING
- Make sure input file path is correct.
- Use 'python3' instead of 'python' if Python 2 is installed.
- Make sure file exist.

24.03.2026 