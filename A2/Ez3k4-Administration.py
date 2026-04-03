#!/usr/bin/env python3

file = "Administration-test1.in"

def parse_administration(file):
    with open(file, "rt") as fh:
        number_of_capitals, cost_limit = fh.readline().rstrip().split()
        number_of_capitals = int(number_of_capitals)
        cost_limit = int(cost_limit)

        capital_list = fh.readline().rstrip().split()

        # Temporary storage for all edges (before pruning)
        edges = []
        min_edge_cost = float("inf")

        # --- Read cost matrix ---
        for i in range(number_of_capitals):
            city_i = capital_list[i]
            row = fh.readline().strip().split()

            for j in range(i + 1, number_of_capitals):
                if row[j] != "-":
                    cost = int(row[j])
                    min_edge_cost = min(min_edge_cost, cost) # compare, choose smaller

                cost = int(row[j])
                city_j = capital_list[j]
                # store edge temporarily
                edges.append((city_i, city_j, cost))

        # Remaining pairs after picking one pair (-> -1)
        remaining_pairs = number_of_capitals // 2 - 1
        min_remaining_cost = remaining_pairs * min_edge_cost # cost to prune pairs with an impossible cost depending on the overall min cost and number of pairs

        # Build adjacency list with pruning, first init city: []
        authority_cost = {city: [] for city in capital_list}
        for city_i, city_j, cost in edges: # access temp list tuples

            # prune edges that can never fit into a valid solution
            if cost > cost_limit - min_remaining_cost:
                continue

            # add edge in both directions (undirected graph) so i dont mess up recursion (each step needs full information)
            authority_cost[city_i].append((city_j, cost))
            authority_cost[city_j].append((city_i, cost))

        return authority_cost, cost_limit, capital_list


def find_pairings(unpaired, graph, budget, current_pairs=None, current_cost=0):
    
    # initialize 
    if current_pairs is None:
        current_pairs = []

    # base case: no cities left
    if len(unpaired) == 0:
        return [current_pairs]

    results = []

    # choose first city (fix order to avoid duplicates)
    city_a = unpaired[0]

    # --- compute simple lower bound (pruning) ---
    # remaining pairs after choosing next pair
    remaining_pairs = (len(unpaired) // 2) - 1

    # update smallest remaining edge from graph
    min_edge = min(cost for neighbors in graph.values() for _, cost in neighbors) # graph.values() = city key, _ = partner city for every recursion
    min_remaining_cost = remaining_pairs * min_edge # number of remaining recursions, min cost

    # try all partners of city_a, get the cost of partner
    for city_b, cost in graph[city_a]:

        # skip if city_b already used
        if city_b not in unpaired:
            continue

        new_cost = current_cost + cost

        # prune to expensive branches 
        if new_cost > budget - min_remaining_cost:
            continue

        # update list of unpaired cities
        remaining = [c for c in unpaired if c not in (city_a, city_b)]

        # recursive call
        results += find_pairings(
            remaining,
            graph,
            budget,
            current_pairs + [(city_a, city_b)],
            new_cost
        )

    return results

if __name__ == "__main__":
    file = "Administration-test1.in"
    authority_cost, cost_limit, capital_list = parse_administration(file)

    authorities = find_pairings(capital_list, authority_cost, cost_limit)
    print(authorities)