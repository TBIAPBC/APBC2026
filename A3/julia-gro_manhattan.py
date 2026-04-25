import sys

def get_file():
    args = sys.argv[1:]  
    trace = '-t' in args
    diagonal = '-d' in args
    filename = [a for a in args if not a.startswith('-')][-1]

    with open(filename, "r") as f:
        text = f.read()
        
    return text, trace, diagonal




def get_data(text, diagonal):   
    all_rows = []
    for line in text.splitlines():
        if line.startswith('#'):
            continue
        line = line.strip()
        if not line:
            continue
        row = [float(x) for x in line.split()]
        all_rows.append(row)

    M = len(max(all_rows, key=len))
    south = [row for row in all_rows if len(row) == M]
    N = len(south) + 1

    remaining = [row for row in all_rows if len(row) == M - 1]

    if diagonal:
        east = remaining[:N]
        diag = remaining[N:]
    else: 
        east = remaining
        diag = None
    
    return south, east, diag, N, M 

def solve(south, east, diag, N, M, diagonal):
    dp = [[0.0] * M for _ in range(N)]

    for j in range(1, M):
        dp[0][j] = dp[0][j-1] + east[0][j-1]

    for i in range(1, N):
        dp[i][0] = dp[i-1][0] + south[i-1][0]

    for i in range(1, N):
        for j in range(1, M):
            from_north = dp[i-1][j] + south[i-1][j]
            from_west = dp[i][j-1] + east[i][j-1]
            if diagonal:
                from_diag = dp[i-1][j-1] + diag[i-1][j-1]
                dp[i][j] = max(from_north, from_west, from_diag)
            else:
                dp[i][j] = max(from_north, from_west)

    return dp

def traceback(dp, south, east, diag, N, M, diagonal):
    i, j = N-1, M-1
    moves = []

    while i>0 or j>0:                                   # "or" because with "and" the loop stops without going through the last steps
        if i == 0:
            moves.append("E")
            j -= 1
        elif j == 0:
            moves.append("S")
            i -= 1
        else: 
            from_north = dp[i-1][j] + south[i-1][j]
            from_west = dp[i][j-1] + east[i][j-1]
            if dp[i][j] == from_north:
                moves.append("S")
                i -= 1
            elif diagonal and dp[i][j] == dp[i-1][j-1] + diag[i-1][j-1]:
                moves.append("D")
                i -= 1
            else:
                moves.append("E")
                j -= 1

    return ''.join(reversed(moves)) 

    

def main():

    text, trace, diagonal = get_file()
    south, east, diag, N, M = get_data(text, diagonal)
    dp = solve(south, east, diag, N, M, diagonal)

    if dp[N-1][M-1].is_integer():
        print(int(dp[N-1][M-1]))  
    else:
        result = dp[N-1][M-1]
        print(f"{result: .2f}")

    if trace:
        path = traceback(dp, south, east, diag, N, M, diagonal)
        print(path)


if __name__ == "__main__":
    main()













