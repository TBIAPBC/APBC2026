import sys


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


Pairing = tuple[str, str]
Solution = list[Pairing]
PairingCosts = dict[str, dict[str, int]]
Node = list[Pairing]
Stack = list[Node]


def cost(node: Node) -> int:
    total = 0
    for pairing in node:
        total += costs[pairing[0]][pairing[1]]
    return total

def optimize() -> list[Solution]:
    # node state: list of commited captital pairings at that node of the tree 
    stack  = [] 
    result = []
    stack.append([])
    while stack:
        node = stack.pop()
        if cost(node) <= cost_limit:
            if len(node) == num_capitals//2:
                result.append(node)
            else:
                stack.extend(split(node))
    result.reverse()
    return result

def split(node: Node) -> list[Node]:
    result = []
    # name lex > erster buchstabe, letztes tupel in der node
    remaining_names = list(filter(lambda name: not node or name > node[-1][0], capital_names))
    for names in node:
        if names[0] in remaining_names:
            remaining_names.remove(names[0])
        if names[1] in remaining_names:
            remaining_names.remove(names[1])
    for i, a in enumerate(remaining_names):
        for j in range(i + 1, len(remaining_names)):
            b = remaining_names[j]
            new_node = node.copy()
            new_node.append((a, b))
            result.append(new_node)
    return result


def format_solutions(solutions: list[Solution]) -> str:
    result = ""
    for solution in solutions:
        for pairing in solution:
            result += pairing[0] + pairing[1] + " "
        result += "\n"
    return result



opt = optimize()
print(format_solutions(opt))
# print(opt)
print(len(opt))

# TODO:
# -o flag
# refactor
# fix print new line
# make readme
