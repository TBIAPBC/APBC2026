# Optimizing the administration of Atirasu

The government of the federal state Atirasu plans to modernize its administration by creating four new authorities for generally unremarkable affairs. These authorities shall be distributed to the **capitals of given provinces** such that **each two provinces share one authority**. Consequently, the set of capitals shall be partitioned into subsets of two elements each.


### How to run the code
`python julia-gro-Administration.py input_file'

**parameter**
- `-o`: the program optimizes the cost (instead of enumerating). The cost limit is used as initial bound. As result it  prints the score of the best solution. 


### Expected Input and Output
**input:** 
first row: number of capitals; cost limit
second row: names of capitals
rest: symmetric cost matrix

*Example*
Input:
14 9
A B C D E F G H I J K L M N
- 3 2 2 8 1 1 6 3 1 1 4 3 7
3 - 8 5 5 1 4 2 8 8 3 4 2 3
2 8 - 7 1 1 3 1 2 8 9 1 6 3
2 5 7 - 3 7 4 3 1 1 2 4 1 3
8 5 1 3 - 3 2 7 5 3 2 8 1 6
1 1 1 7 3 - 2 6 8 8 9 4 3 5
1 4 3 4 2 2 - 8 1 6 5 9 3 7
6 2 1 3 7 6 8 - 6 1 1 9 5 5
3 8 2 1 5 8 1 6 - 4 3 5 8 7
1 8 8 1 3 8 6 1 4 - 5 6 3 4
1 3 9 2 2 9 5 1 3 5 - 3 4 3
4 4 1 4 8 4 9 9 5 6 3 - 2 8
3 2 6 1 1 3 3 5 8 3 4 2 - 5
7 3 3 3 6 5 7 5 7 4 3 8 5 -

**output:**
This script outputs all combination of pairs, where the cost limit is not exceeded. The pairs are listed alphabetically, within the pair and the pairs themselves. When given the parameter `-o` The output is is only a score, the optimization  of cost.

*Example*
AF BN CL DJ EM GI HK
AG BF CL DI EM HJ KN
AJ BF CL DN EM GI HK
AK BF CL DN EM GI HJ

with parameter `-o`:
9