"""
Manhattan Tourist problem 
- horizontal/vertikal instances HV
- horizpontal/vertikal/diagonal instances HVD using -d flag 
- traceback of optimal path usign -t
"""
import argparse
import sys


def parse_args():
    """
    parsing commandline args
    needs the filename and options with -t gives path and with -d using also diagnol edges"""
    parser = argparse.ArgumentParser(description="Solve the Manhattan Tourist Problem")
    parser.add_argument("filename", help="input file")
    parser.add_argument("-t", action="store_true", help="print optimal path")
    parser.add_argument("-d", action="store_true", help="allow/use diagonal weights")
    return parser.parse_args()


def read_file(filename, diagonal=False):
    """
    return grid dimension and weight matrix, ignoring comments and empty lines, also usable on int and float
    - HV: first line is n,m 
    - also only weight matrix without line that tells us size
    - returns: n, m, list of n-1 x m(down), list of n x m-1(right), listt of n-1 x m-1(diag)"""
    data = []

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.split("#")[0].strip()
            if not line:
                continue

            parts = []
            for x in line.split():
                x = x.replace(",", ".")
                try:
                    parts.append(float(x))
                except ValueError:
                    pass

            if parts:
                data.append(parts)

    if not data:
        raise ValueError("input file is empty or contains no valid numbers")
# first case: first line gives n and m 
    if len(data[0]) == 2 and all(v.is_integer() for v in data[0]):
        n = int(data[0][0])
        m = int(data[0][1])

        expected_hv = 1 + (n - 1) + n
        expected_hvd = 1 + (n - 1) + n + (n - 1)

        if diagonal:
            if len(data) < expected_hvd:
                raise ValueError("not enough rows for diagonal input")
        else:
            if len(data) < expected_hv:
                raise ValueError("not enough rows for HV input")

        idx = 1

        down = []
        for _ in range(n - 1):
            row = data[idx]
            if len(row) != m:
                raise ValueError("wrong number of entries in north-south matrix")
            down.append(row)
            idx += 1

        right = []
        for _ in range(n):
            row = data[idx]
            if len(row) != m - 1:
                raise ValueError("wrong number of entries in west-east matrix")
            right.append(row)
            idx += 1

        diag = None
        if diagonal:
            diag = []
            for _ in range(n - 1):
                row = data[idx]
                if len(row) != m - 1:
                    raise ValueError("wrong number of entries in diagonal matrix")
                diag.append(row)
                idx += 1

        return n, m, down, right, diag
# second case only matrix
    m = len(data[0])

    n = 1
    for row in data:
        if len(row) == m:
            n += 1
        else:
            break

    down = []
    for i in range(n - 1):
        if len(data[i]) != m:
            raise ValueError("wrong number of entries in north-south matrix")
        down.append(data[i])

    right = []
    for i in range(n):
        row = data[i + n - 1]
        if len(row) != m - 1:
            raise ValueError("wrong number of entries in west-east matrix")
        right.append(row)
# optional read diagonal
    diag = None
    if diagonal:
        diag = []
        start = 2 * n - 1
        for i in range(n - 1):
            row = data[start + i]
            if len(row) != m - 1:
                raise ValueError("wrong number of entries in diagonal matrix")
            diag.append(row)

    return n, m, down, right, diag


def compute_dp(n, m, down, right, diag=None):
    """dynamic progamming approach trying to reach maximal path 
    recurrent: if first column 0 only moves south, if first row only 0 only east possible, 
    else score for i.j max( 
    score i-1, +down i-1, j
    score i , j-1+ right i, j-1)
    
    with diagonal also score i-1, j-1+ diag i-1, j-1
    
    in previous store move
    """
    scores = [[0.0] * m for _ in range(n)]
    prev = [["X"] * m for _ in range(n)]

    for i in range(1, n):
        scores[i][0] = scores[i - 1][0] + down[i - 1][0]
        prev[i][0] = "S"

    for j in range(1, m):
        scores[0][j] = scores[0][j - 1] + right[0][j - 1]
        prev[0][j] = "E"

    use_diag = diag is not None

    for i in range(1, n):
        for j in range(1, m):
            best_score = scores[i - 1][j] + down[i - 1][j]
            best_move = "S"

            east_score = scores[i][j - 1] + right[i][j - 1]
            if east_score > best_score:
                best_score = east_score
                best_move = "E"

            if use_diag:
                diag_score = scores[i - 1][j - 1] + diag[i - 1][j - 1]
                if diag_score > best_score:
                    best_score = diag_score
                    best_move = "D"

            scores[i][j] = best_score
            prev[i][j] = best_move

    return scores, prev


def traceback(prev):
    """
    reconstruction of path starting bottom right following prev i, j and collect path and reverse
    returns string of S, E, D from start
    """
    i = len(prev) - 1
    j = len(prev[0]) - 1
    path = []

    while prev[i][j] != "X":
        move = prev[i][j]
        path.append(move)

        if move == "S":
            i -= 1
        elif move == "E":
            j -= 1
        else:
            i -= 1
            j -= 1

    path.reverse()
    return "".join(path)


def main():
    """
    1. parse args
    2. read input
    3. run dynamic approach
    4. print score
    5. if -t print path
    """
    args = parse_args()

    try:
        n, m, down, right, diag = read_file(args.filename, args.d)
        scores, prev = compute_dp(n, m, down, right, diag)

        print(f"{scores[-1][-1]:.2f}")

        if args.t:
            print(traceback(prev))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
