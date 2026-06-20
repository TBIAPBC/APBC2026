"""
    Script for Assignment 2 - Administration. 

    This script reads in an input file (name given over the command line).

    The program uses recursive backtracking with Branch and Bound pruning:
        1. Select the first unmatched city.
        2. pair with every possible unmatched city.
        3. update accumulated cost.
        4. prune if:
            - the cost exceeds the allowed limit
            - the edge is invalid
            - cost do not immprove the best known solution (optimization mode)
        5. continue recursively until all cities are paired. 

    Usage: 
        python annadhm-Administration.py <input_file>       #all solutions within cost limits
        python annadhm-Administration.py -o <input_file>    # optimize: prints best cost only
"""
import sys

def extract_infos(filename):
    """
        extract infos from input file and returns cities, cost matrix and cost limit.
    """
    with open(filename) as f:
        lines = [line.strip() for line in f if line.strip()]
    
    # first line: number of cities and cost limit
    first = lines[0].split()
    n, cost_limit = int(first[0]), int(first[1])

    # second line: city names
    cities = lines[1].split()
    assert len(cities) == n, f"{n} cities expected, got {len(cities)}"

    # build cost matrix (n x n)
    cost = [[0] * n for _ in range(n)]
    for i, line in enumerate(lines[2:2 + n]):
        values = line.split()
    
        for j, val in enumerate(values):
            if val == '-':
                cost[i][j] = float('inf')
            else:
                cost[i][j] = int(val)
    
    return n,cost_limit, cities, cost

def pair_key(cities, i, j):
    """
    Returns the sorted string of a pair.
    """
    a, b = cities[i], cities[j]
    return (a + b) if a < b else (b + a)

def partition_key(cities, pairs):
    """
    Return lexicographically smallest string. 
    Each pair is sorted (extern function). 
    The list of pairs is sorted and joined.
    """
    tokens = sorted(pair_key(cities, i, j) for i,j in pairs)
    return " ".join(tokens)

def branch_and_bound(n, cost_limit, cities, cost, optimizer = False): 
    """
        Enumerate (or optimize) matchings on 'cities' whose total cost os strictly ≤ cost limit over branch and bound.

        Approach:
        - Pair the first unmatched city with one of the remaining cities. 
        - Track const, prune as soon as it exceed the bound.
        - optimizer mode: bound is tightened when better solution is found. 
    
        Args: 
        n = int
            - number of cities
        cost_limit = int
            - cost limit
        cities = list
            - list of city names
        cost = list
            - cost matrix
        optimizer = bool
            - optimization mode
        Returns:
            - solutions 
            - best_cost (only in optimization mode)
    """
    solutions = []
    best_cost = [cost_limit]

    # boolean array to save pairs
    matched = [False] * n

    def backtrack(pairs, current_cost):
        # find first unmatched city
        first_free = -1
        for idx in range(n):
            if not matched[idx]:
                first_free = idx
                break
        
        # all cities matched -> solution found
        if first_free == -1:
            if optimizer:
                if current_cost < best_cost[0]:
                    best_cost[0] = current_cost
            else:
                solutions.append(partition_key(cities, pairs))
            return

        # pair first_free with other unmatched city
        matched[first_free] = True
        for pair in range(first_free+1, n):
            if matched[pair]:
                continue

            pair_cost = cost[first_free][pair]

            #directly skip forbidden edges
            if pair_cost == float('inf'):
                continue

            new_cost = current_cost + pair_cost

            # pruning
            if new_cost > cost_limit:
                continue

            if optimizer and new_cost >= best_cost[0]:
                continue

            matched[pair] = True
            pairs.append((first_free, pair))

            backtrack(pairs, new_cost)

            pairs.pop()
            matched[pair] = False

        matched[first_free] = False
    
    backtrack([], 0)

    if optimizer:
        return best_cost[0]
    else:
        return sorted(solutions)


def main():

    # === Read input file === 
    
    args = sys.argv[1:]

    optimizer = False
    if '-o' in args:
        optimizer = True
        args = [a for a in args if a != '-o']
    
    if len(args) != 1:
        print("Invalid flags!")
        print(f"Try: annadhm-Administration.py -o Administration-test*.in")
        sys.exit(1)
    
    filename = args[0]
    n, cost_limit, cities, cost = extract_infos(filename)

    if optimizer:
        best = branch_and_bound(n,cost_limit, cities, cost, optimizer=True)
        print(best)
    else:
        solution = branch_and_bound(n, cost_limit, cities, cost, optimizer=False)
        for s in solution:
            print(s)


if __name__ == "__main__":
    main()