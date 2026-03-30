import argparse
from pdb import run
from typing import ByteString, Dict, Iterable, List, Tuple


#Parse the assignment input file into (cities, limit, cost_dict)
def parse_input(path: str) -> Tuple[List[str], int, Dict[Tuple[str, str], int]]:
    with open(path, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip()]

    if len(lines) < 3:
        raise ValueError("Input file is too short.")

    n_s, limit_s = lines[0].split()
    n = int(n_s)
    limit = int(limit_s)
    if n <= 0 or n % 2 != 0:
        raise ValueError("Number of cities must be positive and even.")

    cities = lines[1].split()
    if len(cities) != n:
        raise ValueError(f"Expected {n} city names, got {len(cities)}.")

    if len(lines) < 2 + n:
        raise ValueError(f"Expected {n} matrix rows.")

    # cost[(min(city_a,city_b), max(city_a,city_b))] = cost_value
    cost: Dict[Tuple[str, str], int] = {}
    for i in range(n):
        row_parts = lines[2 + i].split()
        if len(row_parts) != n:
            raise ValueError(f"Matrix row {i} has wrong length.")

        for j in range(i+1, n):
            cost_ij = row_parts[j]
            if cost_ij == "-":
                raise ValueError(f"Unexpected '-' at row {i}, col {j}.")
            v = int(cost_ij)

            a, b = cities[i], cities[j]
            key = (a, b) if a < b else (b, a)
            cost[key] = v

    return cities, limit, cost


def pair_cost(costs: Dict[Tuple[str, str], int], a: str, b: str) -> int:
    """Returns the matrix cost for the unordered pair {a,b}"""
    key = (a, b) if a < b else (b, a)
    return costs[key]


def canonical_solution_string(pairs: List[Tuple[str, str]]) -> str:
    """Converts a partition into the canonical output format"""
    city_pairs: List[str] = []
    for x, y in pairs:
        a, b = (x, y) if x < y else (y, x)
        city_pairs.append(a + b)
    city_pairs.sort()
    return " ".join(city_pairs)

def find_cheapest_pair(costs: Dict[Tuple[str, str], int]) -> int:
    """Returns the cheapest cost in our matrix to serve as a basic lower bound cost"""
    return min(costs.values())

def compute_solutions(cities: List[str], limit: int, costs: Dict[Tuple[str, str], int], o: bool):
    """If o: Gets lowest cost of all valid solutions
    If not o: Gets canonical solution strings for all valid solutions
    Valid solution = any solution with total cost <= limit"""
    cheapest_cost = find_cheapest_pair(costs)
    best = limit

    def rec(remaining_cities: List[str], chosen: List[Tuple[str, str]], running_cost: int):
        nonlocal best
        remaing_pairs = len(remaining_cities) /2
        if o:
            if running_cost + remaing_pairs * cheapest_cost > best:
                return
        elif running_cost + remaing_pairs * cheapest_cost > limit:
            return

        if not remaining_cities:
            best = running_cost if running_cost < best else best            
            yield best if o else canonical_solution_string(chosen)
            return

        # Fix the first remaining city to avoid duplicates.
        first = remaining_cities[0]
        for i in range(1, len(remaining_cities)):
            second = remaining_cities[i]
            c = pair_cost(costs, first, second)
            next_running_cost = running_cost + c 
            next_remaining = remaining_cities[1:i] + remaining_cities[i + 1 :]
            chosen.append((first, second))
            yield from rec(next_remaining, chosen, next_running_cost)
            chosen.pop()

    yield from rec(cities, [], 0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str, help="Path to the input matrix file")
    parser.add_argument(
        "-o",
        action="store_true",
        help="Optimize (print best score) instead of enumerating partitions",
    )
    args = parser.parse_args()

    cities, limit, cost = parse_input(args.filename)


    solution_output = sorted(compute_solutions(cities, limit, cost, args.o))

    if not solution_output:
        print("No solution found")
    elif args.o:
        print(solution_output[0])
    else:
        for s in solution_output:
            print(s)


if __name__ == "__main__":
    main()