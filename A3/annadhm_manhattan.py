"""
    This script solves the manhattan problem over dynamic programming. 
    It searches for the longest/heaviest path through a weighted grid from the top-left node (0,0)
    to the bottom-right node (n,m), moving only South(S), East(E), and optionally Diagonal(D)

    South moves are prefered over East moves over Diagonal modes.

    Optionally a traceback flag can be enabled: Which records the moves taken to each cell, 
    and recunstructs the path by walking back from (n,m) to (0,0)
"""

import argparse

def format(weight):
    return str(int(weight)) if float(weight).is_integer() else f"{weight:.2f}"

def parse_input(f_name, use_diag= False):
    """
        convert Text file into clean matrices

        down[i][j] -> weight of moving south
        right[i][j] -> weight of moving east
        diagonal[i][j] -> weight of moving diagonal (optional)
    """
    with open(f_name) as f:
        raw_lines = f.readlines()
        
    has_divider = any(line.strip().startswith("#---") for line in raw_lines)

    if has_divider:
        # Case 1: HVD with "----"" divider
        blocks = []
        current = []
        for line in raw_lines:
            raw = line.strip()

            if raw.startswith("#---"):
                if current:
                    blocks.append(current)
                    current = []
                continue
            cleaned = line = line.split("#")[0].strip()
            if cleaned:
                current.append(list(map(float, cleaned.split())))
            
        if current:
            blocks.append(current)
    
        down = blocks[0]
        right = blocks[1]
        diagonal = blocks[2] if use_diag and len(blocks) > 2 else None

        
        # secure HVD format
        assert len(down) == len(right) - 1, (
            f"✋ Wait a minute... South matrix has {len(down)} rows, expected {len(right) - 1}"
        )
        assert len(down[0]) == len(right[0]) +1, (
            f"✋ Hold on ... South matrix has {len(down[0])} collumns, expected {len(right[0]) +1}"     
        )
        if diagonal is not None:
            assert len(diagonal) == len(down), (
                f"✋ CRASH... Diagonal has {len(diagonal)} rows, expected {len(down)}"
        )
            assert len(diagonal[0]) == len(right[0]), (
                f"✋ UPS... Diagonal has {len(diagonal[0])} cols, expected {len(right[0])}"
        )
        return down, right, diagonal

    # Case 2: HV without divider
        # down has the same amount of columns as right + 1
    lines = []
    for line in raw_lines:
        cleaned = line.split("#")[0].strip()
        if cleaned:
            lines.append(cleaned)

        
    rows = [list(map(float, line.split())) for line in lines]
    
    for split in range(1, len(rows)):
        down = rows[:split]
        right = rows[split:]

        # check dimensions
        if len(down) > 0 and len(right) > 0:
            m = len(down[0])
            if all(len(r) == m for r in down) and all(len(r) == m-1 for r in right):
                assert len(down) == len(right) - 1, (
                    f"✋ Wait a minute... South matrix has {len(down)} rows, expected {len(right) - 1}"
                )
                assert len(down[0]) == len(right[0]) +1, (
                    f"✋ Hold on ... South matrix has {len(down[0])} collumns, expected {len(right[0]) +1}"     
                )
                return down, right, None
    
    raise ValueError("✋ You should not pass! -- input file couldn't be parsed")    


def manhatten_problem(down, right, diagonal=None, traceback = False):
    n = len(down)
    m = len(right[0])

    dp = [[0]*(m+1) for _ in range(n+1)] # dp = best score to reach node (i,j)
    parent = [[None]*(m+1) for _ in range(n+1)] # backtracking path

    # initialize first column -> only "S" moves
    for i in range(1, n+1):
        dp[i][0] = dp[i-1][0] + down[i-1][0]
        parent[i][0] = 'S'
    
    # initialize first row -> only "E" moves
    for j in range(1, m+1):
        dp[0][j] = dp[0][j-1] + right[0][j-1]
        parent[0][j] = 'E'
    
    # fill DP
    order = {'S':0, 'E':1, 'D':2}
    for i in range(1, n+1):
        for j in range(1, m+1):
            # HV version
            options=[
                (dp[i-1][j] + down[i-1][j], 'S'),
                (dp[i][j-1] + right[i][j-1], 'E')
            ]
            # HVD version
            if diagonal is not None:
                options.append((dp[i-1][j-1] + diagonal[i-1][j-1], 'D'))

            # Pick the best
            # maximize score and prefer S over E over D
            options.sort(key=lambda x: (-x[0], order[x[1]]))

            dp[i][j], parent[i][j] = options[0] 
    
    if not traceback:
        return dp[n][m]
    
    # Traceback
    path = []
    i, j = n, m

    while i > 0 or j > 0:
        move = parent[i][j]
        path.append(move)

        if move == 'S':
            i -= 1
        elif move == 'E':
            j -= 1
        else: #D
            i -= 1
            j -= 1
    
    return dp[n][m], ''.join(reversed(path))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("-d", action="store_true")
    parser.add_argument("-t", action="store_true")

    args = parser.parse_args()

    down, right, diagonal = parse_input(args.file, args.d)
    if args.d and diagonal is None:
        print("⚠️ Warning: I am missing diagonal weights - Falling back to HV default mode")

    if args.t:
        weight, path = manhatten_problem(down, right, diagonal, True)
        print(format(weight))
        print(path)
    else:
        weight = manhatten_problem(down, right, diagonal)
        print(format(weight))

if __name__ == "__main__":
    main()