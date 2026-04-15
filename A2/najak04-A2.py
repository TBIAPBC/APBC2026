import sys


def read_instance(f):
    first = f.readline().strip()
    if not first:
        raise ValueError("empty file")

    parts = first.split()
    if len(parts) != 2:
        raise ValueError("first line must contain n and cost limit")

    n = int(parts[0])
    cost_limit = int(parts[1])

    cities = f.readline().split()
    if len(cities) != n:
        raise ValueError("number of city names does not match n")

    costs = []
    for _ in range(n):
        row_parts = f.readline().split()
        if len(row_parts) != n:
            raise ValueError("row length does not match n")

        row = []
        for x in row_parts:
            if x == "-":
                row.append(0)
            else:
                row.append(int(x))
        costs.append(row)

    return n, cost_limit, cities, costs


def canonical_solution(pairs):
    pair_strings = []

    for a, b in pairs:
        if a < b:
            pair_strings.append(a + b)
        else:
            pair_strings.append(b + a)

    pair_strings.sort()
    return " ".join(pair_strings)


def enumerate_solutions(remaining, current_pairs, current_cost,
                        bound, costs, index, results):
    if not remaining:
        results.append(canonical_solution(current_pairs))
        return

    first = remaining[0]

    for i in range(1, len(remaining)):
        other = remaining[i]
        pair_cost = costs[index[first]][index[other]]
        new_cost = current_cost + pair_cost

        if new_cost > bound:
            continue

        new_remaining = remaining[1:i] + remaining[i + 1:]
        enumerate_solutions(
            new_remaining,
            current_pairs + [(first, other)],
            new_cost,
            bound,
            costs,
            index,
            results,
        )


def optimize_solution(remaining, current_cost, best_cost, costs, index):
    if not remaining:
        return current_cost

    first = remaining[0]
    best = best_cost

    for i in range(1, len(remaining)):
        other = remaining[i]
        pair_cost = costs[index[first]][index[other]]
        new_cost = current_cost + pair_cost

        if new_cost >= best:
            continue

        new_remaining = remaining[1:i] + remaining[i + 1:]
        candidate = optimize_solution(
            new_remaining,
            new_cost,
            best,
            costs,
            index,
        )

        if candidate < best:
            best = candidate

    return best


def main():
    args = sys.argv[1:]

    optimize = False
    if len(args) == 2 and args[0] == "-o":
        optimize = True
        infile = args[1]
    elif len(args) == 1:
        infile = args[0]
    else:
        print("Usage: python a2.py [-o] <inputfile>")
        sys.exit(1)

    with open(infile, "r") as f:
        n, cost_limit, cities, costs = read_instance(f)

    if n % 2 != 0:
        raise ValueError("number of cities must be even")

    index = {}
    for i, name in enumerate(cities):
        index[name] = i

    if optimize:
        best = optimize_solution(cities, 0, cost_limit + 1, costs, index)
        if best <= cost_limit:
            print(best)
    else:
        results = []
        enumerate_solutions(cities, [], 0, cost_limit, costs, index, results)

        for line in sorted(set(results)):
            print(line)


if __name__ == "__main__":
    main()
