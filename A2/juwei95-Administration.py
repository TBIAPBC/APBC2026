import sys
from math import inf


# Input

lines = sys.stdin.readlines()

num_capitals = int(lines[0].split()[0])
cost_limit = int(lines[0].split()[1])
capital_names = lines[1].split()
costs = {}

for i, line in enumerate(lines[2:]):
    key = capital_names[i]
    value = {}
    for j, cost in enumerate(line.split()):
        if cost != "-":
            value.update({capital_names[j]: int(cost)})
    costs.update({key: value})

dash_o = "-o" in sys.argv

# Type definitions
Pairing = tuple[str, str]
Solution = list[Pairing]
PairingCosts = dict[str, dict[str, int]]
Node = list[Pairing] # node state: list of commited captital pairings at that node of the tree
Stack = list[Node]

def optimize() -> list[Solution]:
    """
    Perform a depth-first search over all possible capital pairings.
    For each valid complete pairing, it records the solution and 
    updates the best (lowest) cost found.
    """

    best = inf
    best_node = None
    stack  = [] 
    result = []
    stack.append([])
    while stack:
        node = stack.pop()
        node_cost = calc_node_cost(node)
        if node_cost <= cost_limit:
            if node_cost + bound(node) < best or not dash_o:
                if len(node) == num_capitals//2:
                    result.append(node)
                    best = node_cost
                    best_node = node
                else:
                    stack.extend(branch(node))
    result.reverse()
    if dash_o:
        return [best_node]
    else:
        return result

def bound(node: Node) -> float:
    total = 0
    remaining_names = get_remaining_names(node)
    for n in remaining_names:
        min_cost = None
        for m in remaining_names:
            if n != m:
                cost = costs[n][m]
                if min_cost is None or cost < min_cost:
                    min_cost = cost
        if min_cost is not None:
            total += min_cost
    return total / 2

def get_remaining_names(node: Node) -> list[str]:
    remaining_names = capital_names.copy()
    for names in node:
        if names[0] in remaining_names:
            remaining_names.remove(names[0])
        if names[1] in remaining_names:
            remaining_names.remove(names[1])
    return remaining_names

def calc_node_cost(node: Node) -> int:
    total = 0
    for pairing in node:
        total += costs[pairing[0]][pairing[1]]
    return total

def branch(node: Node) -> list[Node]:
    result = []
    # name lex > first character of last tuple in node
    remaining_names = list(filter(lambda name: not node or name > node[-1][0], get_remaining_names(node)))
    for i, a in enumerate(remaining_names):
        for j in range(i + 1, len(remaining_names)):
            b = remaining_names[j]
            new_node = node.copy()
            new_node.append((a, b))
            result.append(new_node)
    return result

def format_solutions(solutions: list[Solution]) -> str:
    result = []
    for solution in solutions:
        pair = ""
        if dash_o:
            pair += str(calc_node_cost(solution))
        else:
            for pairing in solution:
                pair += (pairing[0] + pairing[1] + " ")
        result.append(pair)
    return "\n".join(result)

# Run the algorithm
opt = optimize()
print(format_solutions(opt))
