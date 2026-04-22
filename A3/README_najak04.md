# Manhattan Tourist Problem Solver

This program solves the **Manhattan Tourist Problem** by dynamic programming, so it breaks it down to subproblems which here is the maximum path to the next neighbouring crossing.  
We are given a grid-like street network (junctions connected by streets), and each street has a weight (e.g. number of sights).  
The goal is to find a path from the top-left to the bottom-right corner with **maximum total weight as the tourist wants to see most sights**.

The tourist can always move **east (E)** or **south (S)**, and optionally also **diagonally (D)** if diagonal edges are provided and the -d flagh is given.

---

## Features

- Supports **HV** instances (horizontal/vertical moves only).
- Supports **HVD** instances (horizontal/vertical/diagonal) when run with `-d`.
- Ignores comments and empty lines in the input file.
- Accepts integer and floating point weights (both `.` and `,` as decimal separator).
- Can print the **maximum path weight** and, optionally when run with -t flag, the corresponding **path**.

---

## Usage

python3 najak04.py [options -t, -d] <inputfile>

it will print the results and depending on the -d or -t flag for axample a diagnoal is possible. 
