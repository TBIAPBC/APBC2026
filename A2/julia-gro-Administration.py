import sys

def get_file():
    filename = sys.argv[1]
    with open(filename, "r") as f:
        text = f.read()
    return text

def get_data(input):        
    data = []

    for line in input.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        data.append(parts)

    capital_numbers = int(data[0][0])
    cost_limit = int(data[0][1]) 
    capital_names = data[1]
    matrix = data[2:]

    return capital_numbers, cost_limit, capital_names, matrix

def branch_and_bound(capital_names, matrix, cost_limit, optimize = False):
    decided = []
    remaining = capital_names
    cost_so_far = 0
    node = [decided, remaining, cost_so_far]
    stack = [node]
    best = cost_limit if optimize else float('inf')
    solutions = []

    while stack:
        decided, remaining, cost_so_far = stack.pop()

        if len(remaining) == 0:                                     # is it a complete solution? 
            if optimize:
                if cost_so_far < best: 
                    best = cost_so_far        

            else:
                if cost_so_far <= cost_limit:
                    sorted_pairs = sorted([sorted(pair) for pair in decided])
                    result = " ".join("".join(pair) for pair in sorted_pairs)
                    solutions.append(result)
            

        elif optimize and cost_so_far >= best:
            continue
        elif not optimize and cost_so_far > cost_limit:
            continue
        

        else:
            first = remaining[0]
            partners = remaining[1:]

            for partner in partners:
                pair = (first, partner)
                row = capital_names.index(first)
                col = capital_names.index(partner)
                if matrix[row][col] == "-":
                    continue   
                cost = int(matrix[row][col])

                new_remaining = [c for c in partners if c != partner]
                new_cost = cost_so_far + cost
                new_decided = decided + [pair]

                child_node = [new_decided,  new_remaining, new_cost]
                stack.append(child_node)
    if optimize:
        print(best)
    else:
        for solution in sorted(solutions):
            print(solution)

    return cost_so_far, best, decided
        


def main():
    text = get_file()
    capital_numbers, cost_limit, capital_names, matrix = get_data(text)
    #branch_and_bound(capital_names, matrix, cost_limit)
    #cost_so_far, best, decided = branch_and_bound(capital_names, best, decided)
    

    if "-o" in sys.argv:
        branch_and_bound(capital_names, matrix, cost_limit, optimize=True)
    else:
        branch_and_bound(capital_names, matrix, cost_limit)
    
    """print(f"number of capitals: {capital_numbers }")
    print(f"cost limit: {cost_limit }")
    print(f"capital names: {capital_names }")
    print(f"matrix: {matrix }")
    """
    


if __name__ == "__main__": 
    main()



'''
input: 
first row: number of capitals; cost limit
second row: names of capitals
rest: symmetric cost matrix
'''

'''
When given the flag -o, the program must optimize the cost (instead
of enumerating). The cost limit should be used as initial bound. As
result it must simply print the score of the best solution.
'''