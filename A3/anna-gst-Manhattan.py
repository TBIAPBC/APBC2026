### Date: 21.04.26
### Author: Anna Gsteu
### Description: A3 - Manhattan Tourist Problem with dynamic programming.
###              Reads a grid of street weights and finds the max-weight path
###              from top-left to bottom-right. Flags: -d for diagonals, -t for path,
###              -v to print the dp matrix.


# importing packages
import sys
import argparse

# Parses input text into a list of matrices
def parse_input(text):
    matrices = []
    current_rows = []

    for line in text.splitlines():
        # strips comments and whitespace
        cleaned = line.split("#", 1)[0].strip()  # the 1 helps with efficiency

        if cleaned == "":
            # appends to matrices if current is already filled
            if current_rows:
                matrices.append(current_rows)
                current_rows = []
        else:
            # handles European decimal comma (idea from looking at @Ez3k4 A3 assignemnt)
            row = [float(x.replace(",", ".")) for x in cleaned.split()]

            # detects block boundary: this is set by row length change --> only way to easliy detect change
            if current_rows and len(row) != len(current_rows[-1]):
                matrices.append(current_rows)
                current_rows = []

            current_rows.append(row)

    if current_rows:
        matrices.append(current_rows)

    return matrices

# Reades in input files
def read_input(filename):
    try:
        with open(filename, encoding='utf-8') as f:
            return f.read()
    except OSError as e:
        print(f'Error opening file {e}')
        sys.exit(1)


# Fills the dp matrix
def fill_dp(down, right, diag):
    N = len(right)
    M = len(down[0])
    dp = [[0.0] * M for _ in range(N)]

    # first row: only eastward moves
    for j in range(1, M):
        dp[0][j] = dp[0][j-1] + right[0][j-1]

    # first column: only southward moves
    for i in range(1, N):
        dp[i][0] = dp[i-1][0] + down[i-1][0]

    # inner cells
    if diag is not None:
        for i in range(1, N):
            for j in range(1, M):
                from_above = dp[i-1][j]   + down[i-1][j]
                from_left  = dp[i][j-1]   + right[i][j-1]
                from_diag  = dp[i-1][j-1] + diag[i-1][j-1]
                dp[i][j] = max(from_above, from_left, from_diag)
    else:
        for i in range(1, N):
            for j in range(1, M):
                from_above = dp[i-1][j] + down[i-1][j]
                from_left  = dp[i][j-1] + right[i][j-1]
                dp[i][j] = max(from_above, from_left)

    return dp


# Walking back through dp to reconstruct the path
def traceback(dp, down, right, diag):
    N = len(dp)
    M = len(dp[0])
    moves = []
    i, j = N - 1, M - 1

    while (i, j) != (0, 0):
        # border cases
        if i == 0:
            moves.append('E')
            j -= 1
        elif j == 0:
            moves.append('S')
            i -= 1
        else:
            # south first (tourist prefers south)
            from_above = dp[i-1][j] + down[i-1][j]
            from_left = dp[i][j-1] + right[i][j-1]

            if dp[i][j] == from_above:
                moves.append('S')
                i -= 1
            elif diag is not None and dp[i][j] == dp[i-1][j-1] + diag[i-1][j-1]:
                moves.append('D')
                i -= 1
                j -= 1
            else:
                moves.append('E')
                j -= 1

    moves.reverse()
    return "".join(moves)


# Prints the dp matrix
def print_dp(dp):
    for row in dp:
        print("  ".join(f"{v:7.2f}" for v in row))


def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument(
        'filename', 
        help='input file'
        )
    parser.add_argument(
        '-d', 
        help='diagonal mode', 
        action='store_true'
        )
    parser.add_argument(
        '-t', 
        help='traceback mode', 
        action='store_true'
        )
    parser.add_argument(
        '-m', 
        help='print the dp matrix', 
        action='store_true'
        )
    args = parser.parse_args()

    text = read_input(args.filename)
    matrices = parse_input(text)

    # checks that matrices make sense
    if len(matrices) < 2:
        print("Error: input file must contain at least 2 matrices", file=sys.stderr)
        sys.exit(1)

    if args.d and len(matrices) < 3:
        print("Error: -d flag set but input file has no diagonal matrix", file=sys.stderr)
        sys.exit(1)

    down = matrices[0]
    right = matrices[1]
    diag = matrices[2] if args.d else None

    # shape check
    N = len(right)
    M = len(down[0])
    if len(down) != N - 1 or len(right[0]) != M - 1:
        print("Error: down/right matrix shapes don't match", file=sys.stderr)
        sys.exit(1)
    if diag is not None and (len(diag) != N - 1 or len(diag[0]) != M - 1):
        print("Error: diag matrix shape doesn't match", file=sys.stderr)
        sys.exit(1)

    dp = fill_dp(down, right, diag)

    # prints dp matrix if -m
    if args.m:
        print_dp(dp)

    # rounding of results based on results
    result = dp[-1][-1]
    if result == int(result):
        print(int(result))
    else:
        print(f"{result:.2f}")

    # print path if -t flag is set
    if args.t:
        path = traceback(dp, down, right, diag)
        print(path)


if __name__ == "__main__":
    main()