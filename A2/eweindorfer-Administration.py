

import argparse
from typing import Dict, Iterable, List, Tuple


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


def pair_cost(cost: Dict[Tuple[str, str], int], a: str, b: str) -> int:
    """Returns the matrix cost for the unordered pair {a,b}"""
    key = (a, b) if a < b else (b, a)
    return cost[key]


def canonical_solution_string(pairs: List[Tuple[str, str]]) -> str:
    """Converts a partition into the canonical output format"""
    city_pairs: List[str] = []
    for x, y in pairs:
        a, b = (x, y) if x < y else (y, x)
        city_pairs.append(a + b)
    city_pairs.sort()
    return " ".join(city_pairs)


def enumerate_solutions(
    cities: List[str], limit: int, costs: Dict[Tuple[str, str], int]
) -> Iterable[str]:
    """Gets canonical solution strings for all partitions with total cost <= limit"""

    def rec(remaining_cities: List[str], chosen: List[Tuple[str, str]], running_cost: int):
        if running_cost > limit:
            return
        if not remaining_cities:
            yield canonical_solution_string(chosen)
            return

        # Fix the first remaining city to avoid duplicates.
        first = remaining_cities[0]
        for i in range(1, len(remaining_cities)):
            second = remaining_cities[i]
            c = pair_cost(costs, first, second)
            next_running_cost = running_cost + c
            if next_running_cost > limit:
                continue

            next_remaining = remaining_cities[1:i] + remaining_cities[i + 1 :]
            chosen.append((first, second))
            yield from rec(next_remaining, chosen, next_running_cost)
            chosen.pop()

    yield from rec(cities, [], 0)


def optimize(cities: List[str], limit: int, cost: Dict[Tuple[str, str], int]) -> int:
    """Branch-and-bound search for the minimum total cost"""
    best = limit
    found_any = False

    #recursive function
    def rec(remaining_cities: List[str], running_cost: int):
        nonlocal best, found_any
        if running_cost >= best:
            return
        if not remaining_cities:
            found_any = True
            best = running_cost
            return

        #iteratively try all pairs for the city at position 0
        first = remaining_cities[0]
        for i in range(1, len(remaining_cities)):
            second = remaining_cities[i]
            c = pair_cost(cost, first, second)
            next_running_cost = running_cost + c
            if next_running_cost >= best:
                continue
            
            #when we find a possible pair we go deeper in the branch and continue with the reduced list of cities
            next_remaining = remaining_cities[1:i] + remaining_cities[i + 1 :]
            rec(next_remaining, next_running_cost)

    rec(cities, 0)
    return best if found_any else None


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

    if args.o:
        print(optimize(cities, limit, cost))
        return

    solutions = sorted(enumerate_solutions(cities, limit, cost))
    if not solutions:
        print("No solutions found")
        return
        
    for s in solutions:
        print(s)


if __name__ == "__main__":
    main()
