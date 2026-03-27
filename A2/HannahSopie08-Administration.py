import sys

"""
read file and save content in corresponding variables
Expected file format:
    Line 1: <number of cities> <cost limit>
    Line 2: <city label 1> <city label 2> ...
    Line 3+: cost matrix 
""" 
def read_file(filename): 
    
    number_cities = 0
    cost_limit = 0
    labels = []
    matrix = []

    with open(filename, "r") as f:
        # First line: two numbers
        number_cities, cost_limit = map(int, f.readline().split())
        # Second line: labels
        labels = f.readline().split()

        # Remaining lines: matrix
        for line in f:
            row = []
            for i in line.split():
                if i == "-":
                    row.append(None)   
                else:
                    row.append(int(i))
            matrix.append(row)

    return number_cities, cost_limit, labels, matrix 


def cost_of_pair(i, j, matrix): 
    return matrix[i][j]


"""
Estimate for lower bound cost for pairing of remaining cities
Assumes each city independently pairs with the cheapest partner.
Is not accurate but an easy estimate.
=> Find the cheapest partner for each city among remaining cities, 
if the current cost in combination with the lower_bound exceeds the limit, 
the tree is pruned 
"""
def lower_bound(remaining, matrix): 

    if not remaining: # if no cities are remaining, a cost of 0 is returned 
        return 0
    
    total = 0

    for i in remaining:
        min_cost = None
        for j in remaining: #finds cheapest partner for each city
            if i == j:
                continue
            c = matrix[i][j]
            if c is not None and (min_cost is None or c < min_cost):
                min_cost = c
        
        if min_cost is not None:
            total += min_cost

    return total // 2 # divide by 2, because pairs get counted twice 


# Sort a pair alphabetically
def sort_pair(i, j, labels):
    
    a, b = labels[i], labels[j]
    return (a + b) if a < b else (b + a)


# Sort list of pairs alphabetically
def sort_pairs(pairs, labels):

    pairs_sorted = sorted(sort_pair(i, j, labels) for i, j in pairs)
    return " ".join(pairs_sorted)


"""
Find pairs either within cost limit (if option optimize is not given) or returns only minimum cost partition
(if option optimize given).
Uses recursive branch-and-bound, and prunes the tree when next steps would lead to the cost being over the limit (without optimize) 
or if the current soultion isn't better than the solutions before (with optimize). 
Parameters: 
- labels: list of city names
- matrix: cost matrix
- cost_limit: maximum allowed total cost
- optimize: if True, only partition with best cost is searched instead of finding all solutions within cost limit 
"""
def find_pairs(labels, matrix, cost_limit, optimize):

    n = len(labels)
    solutions = []

    best_cost = [cost_limit]

    #recursive backtrack function
    def backtrack(remaining, current_pairs, current_cost):

        # prune tree if cost larger than limit
        if current_cost > best_cost[0]: 
            return 

        # when all cities are in pairs, save solution
        if not remaining:
            if optimize: 
                if current_cost < best_cost[0]:
                    best_cost[0] = current_cost
                    solutions.clear()
                    solutions.append(current_cost)
                elif current_cost == best_cost[0]:
                    solutions.append(current_cost)
            else:
                solutions.append(sort_pairs(current_pairs, labels))
            return 
        
        # branch-an-bound: if current cost + lower_bound is larger than limit => prune
        if current_cost + lower_bound(remaining, matrix) > cost_limit:
            return 
        
        i = remaining[0]
        rest = remaining[1:]

        # recursive call of function
        for idx, partner in enumerate(rest):
            pair_cost = cost_of_pair(i, partner, matrix)
            if pair_cost is None:
                continue
            new_remaining = rest[:idx] + rest[idx + 1:]
            backtrack(new_remaining, current_pairs + [(i, partner)], current_cost + pair_cost)

    remaining = tuple(range(n))
    backtrack(remaining, [], 0)
    
    return solutions
        
        

def main():

    optimize = "-o" in sys.argv 
    args = [a for a in sys.argv[1:] if a != "-o"]

    filename = args[0]
    output_file = args[1] if len(args) > 1 else None

    number_cities, cost_limit, labels, matrix = read_file(filename)

    if number_cities % 2 != 0:
        print("Error: number of cities is uneven!")
        sys.exit(1)

    
    solutions = find_pairs(labels, matrix, cost_limit, optimize)

    if optimize:
        result = str(solutions[0]) 
    else:
        result = sorted(set(solutions))
    
    
    if output_file:
        with open(output_file, "w") as f:
            f.write("\n".join(result) + "\n")
    else:
        print("\n".join(result))


main()
