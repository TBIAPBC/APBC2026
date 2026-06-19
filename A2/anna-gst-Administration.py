### Date: 07.04.26
### Author: Anna Gsteu
### Description: A2 - Partitions a set of cities into pairs and finds all combinations that stay within a given cost budget. Uses branch and bound to prune expensive paths early. With -o flag, finds the cheapest solution.

import sys
import argparse

def main():
    # parsing input file
    parser = argparse.ArgumentParser(description='Finds all valid pairings of cities within a cost budget.')
    parser.add_argument(
        'filename',
        help='input file'
        )
    parser.add_argument(
        '-o',
        action='store_true',
        help='optimises costs'
        )
    args = parser.parse_args()

    try:
        with open(args.filename, encoding='utf-8') as f:
            text = f.read()
    except OSError as e:
        print(f'Error opening file {e}')
        sys.exit(1)
        
    lines = text.strip().split('\n')
    
    # check if input file follows correct pattern
    if len(lines) < 3:
        print("Error: Invalid input format. Expected:")
        print("  8 10              (number of cities and cost limit)")
        print("  B E G I K L P S   (city names)")
        print("  - 10 10 2 ...     (cost matrix)")
        sys.exit(1)

    # 1st line: number of cities + cost limit
    n, limit = map(int, lines[0].split())

    # 2nd line: city names
    cities = lines[1].split()
    
    # does the city count match
    if len(cities) != n:
        print(f"Error: Header says {n} cities, but found {len(cities)}")
        sys.exit(1)
    
    # do matrix dimensions match
    if len(lines[2:]) != n:
        print(f"Error: Expected {n} matrix rows, but found {len(lines[2:])}")
        sys.exit(1)

    # rest: cost matrix
    # '-' on diagonal means 0
    cost = []
    for line in lines[2:]:
        row = [0 if val == '-' else int(val) for val in line.split()]
        if len(row) != n:
            print(f"Error: Matrix row has {len(row)} values, expected {n}")
            sys.exit(1)
        cost.append(row)
        
    # recursive search: pair cities, prune if over budget
    def search(unpaired, pairs, cost_atm):
        # all paired --> save solution
        if len(unpaired) == 0:
            solutions.append(pairs[:])
            return 
        
        # always picks first unpaired city
        first = unpaired[0]
        rest = unpaired[1:]
        
        # tries every possible partner
        for i in range(len(rest)):
            partner = rest[i]
            pair_cost = cost[cities.index(first)][cities.index(partner)]
            new_cost = cost_atm + pair_cost
            
            # skips if too expensive (branch and bound)
            if new_cost > limit:
                continue
            
            # removes partner from remaining, go deeper
            new_unpaired = rest[:i] + rest[i+1:]
            search(new_unpaired, pairs + [first + partner], new_cost)

    # -o flag: find cheapest solution
    if args.o:
        best_cost = limit
        found = False # takes care that a solution under the limit could actually be found 
        
        def search_opt(unpaired, pairs, cost_atm):
            nonlocal best_cost, found 
            if len(unpaired) == 0:
                # tightens the bound when there is a better solution
                if cost_atm <= best_cost:
                    best_cost = cost_atm
                    found = True
                return
            
            first = unpaired[0]
            rest = unpaired[1:]
            for i in range(len(rest)):
                partner = rest[i]
                pair_cost = cost[cities.index(first)][cities.index(partner)]
                new_cost = cost_atm + pair_cost
                if new_cost > best_cost:
                    continue
                    
                new_unpaired = rest[:i] + rest[i+1:]
                search_opt(new_unpaired, pairs + [first + partner], new_cost)
        
        search_opt(cities, [], 0)
        if found:
            print(best_cost)
        else:
            print("No solution found")
        
    else: 
        # find all solutions within budget
        solutions = []
        search(cities, [], 0)
        for s in solutions:
            print(' '.join(s))

if __name__ == "__main__":
    main()