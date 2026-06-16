import sys


def pairings(free_cities, current_pairs, current_cost):
    k = len(free_cities)
    global limit
    
    if k == 0:
        if optimize:
            #define new limit, if one pairing has less costs
            if current_cost < limit:
                limit = current_cost
        else:
            print_pairs(sorted(current_pairs))
        return

    first = free_cities[0]
    

    for i in range(1, k):
        #pair with the next free city
        partner = free_cities[i]
        
        new_cost = current_cost + costs[first][partner]
        #each pairing costs at least 1, the new pairing has not yet been subtracted
        if new_cost > limit - (k - 2) / 2:
            continue
        
        pairings(free_cities[1:i] + free_cities[i+1:], current_pairs + [(first, partner)], new_cost)


def print_pairs(pairs):
    parts = []
    
    for a, b in pairs:
        parts.append(a + b)
    
    print(" ".join(parts))


filename = sys.argv[1]   
 
optimize = False
if len(sys.argv) > 2 and sys.argv[2] == "-o":
    optimize = True
    
with open(filename, "r", encoding="utf-8") as f:
    lines = f.readlines()

first_line = lines[0].strip().split()

n = int(first_line[0]) #number of provinces
limit = int(first_line[1]) #maximum cost

cities = lines[1].strip().split()

#cost matrix as dictionary, only store upper triangular matrix
costs = {}

for i in range(2, len(lines)):
    values = lines[i].strip().split()
    city = cities[i - 2]

    costs[city] = {}

    for j in range(i - 1, len(values)):
        costs[city][cities[j]] = int(values[j])
        
        
pairings(cities, [], 0)
if optimize:
    print(limit)