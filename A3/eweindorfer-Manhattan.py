import argparse
import os
os.system('')

def main():
    #TODO: add option to ignore diagonal values even when they are given
    #TODO: add simple test file to check direction prio
    #TODO: add readme
    parser = argparse.ArgumentParser(description="Solve Manhattan Tourist Problem")
    parser.add_argument('filename', type=str, help='Input filename')
    parser.add_argument('-t', action='store_true', help='Show optimal path')
    parser.add_argument('-d', action='store_true', help='Use diagonal weights in calculation')
    parser.add_argument('-debug', action='store_true', help='Enable debug printing')
    args = parser.parse_args()


    weights = read_weights(args.filename, args.d)
    if args.debug: print_weights(weights[0], weights[1], weights[2])

    score_matrix = calculate_score_matrix(weights[0], weights[1], weights[2], args.t, debug=args.debug)

    print(round(score_matrix[-1][-1][0],2)) # print final score

    if args.t:
        print_path(score_matrix)



def read_weights(filename, d):
    """
    Reads the input file for the Manhattan Tourist Problem.
        - comments are completely ignored
    Input:
        -filename (str): location of input file
        -d (bool): does file contain diagonal weights or not
    Expects:
        - input file with 2 or 3 weight matrices
            - 3 if d, 2 if not
        - matrix North-South with dimensions m-1 x n
        - matrix East-West with dimensions m x n-1
        - matrix Diagonals with dimensions m-1 x n-1
        - weights have to be valid floating point numbers, invalid entries are ignored
    Returns:
        down: 2D list of north-south edge weights (m-1 rows x n columns)
        right: 2D list of east-west edge weights (m rows x n-1 columns)
        diag: 2D list of diagonal edge weights (m-1 rows x n-1 columns) (if d is set), else None
    """
    def parse_numbers(line):
        return [float(x.replace(',', '.')) for x in line.strip().split() if is_number(x)]

    # check if valid float
    def is_number(s):
        try:
            float(s.replace(',', '.'))
            return True
        except ValueError:
            return False

    with open(filename, 'r') as f:
        lines = []
        for line in f:
            line = line.split('#')[0].strip() # only read in text before '#', i.e. ignore comments
            if line:
                lines.append(line)

    n = len(parse_numbers(lines[0])) # number of junction nodes east-west = number of columns in input line 1

    # m = number of junction nodes north-south -> total number of input lines is either (m-1 + m) or (m-1 + m + m-1)
    if not d and (len(lines)+1)%2 != 0:
        print(f"\033[91mInvalid Input: Number of rows for non-diagonal weight matrix has to total m-1 + m\033[0m")
        exit()
    elif d and (len(lines)+2)%3 != 0:
        print(f"\033[91mInvalid Input: Number of rows for diagonal weight matrix has to total m-1 + m + m-1\033[0m")
        exit()
        
    m = int((len(lines) + 1)/2) if not d else int((len(lines) + 2)/3) 
    down = []
    for i in range(0, m-1):
        new_line = parse_numbers(lines[i])
        if len(new_line) != n:
            print(f"\033[91mExpected {n} valid entries in north-south value matrix but found {len(new_line)} entries in line {i+1}\033[0m")
            exit()
        down.append(new_line) # m-1 entries
    
    right = []
    for i in range(m-1, 2*m - 1):
        new_line = parse_numbers(lines[i])
        if len(new_line) != n-1:
            print(f"\033[91mExpected {n-1} valid entries in east-west value matrix but found {len(new_line)} entries in line {i+1}\033[0m")
            exit()
        right.append(new_line) # m entries
    
    if d:
        diag = []
        for i in range(2*m -1, 3*m -2):
            new_line = parse_numbers(lines[i])
            if len(new_line) != n-1:
                print(f"\033[91mExpected {n-1} valid entries in diagonal value matrix but found {len(new_line)} entries in line {i+1}\033[0m")
                exit()
            diag.append(new_line) # m-1 entries

    else:
        diag = None

    return down, right, diag

def print_weights(down, right, diag):
    print("down:")
    for row in down:
        print(row)
    print("right:")
    for row in right:
        print(row)
    if diag is not None:
        print("diag:")
        for row in diag:
            print(row)

def calculate_score_matrix(down, right, diag, t, debug=False):
    m = len(right) # east-west nodes
    n = len(down[0]) # north-south nodes

    # init m x n score matrix
    # score is a tuple of [score, direction], where direction keeps track of how we entered this node
    score_matrix = [[[0, 'x'] for _ in range(n)] for _ in range(m)] 

    for i in range(1,m): # init first column
        score_matrix[i][0] = [score_matrix[i-1][0][0] + down[i-1][0], 'S']
    for i in range(1,n): #init first row
        score_matrix[0][i] = [score_matrix[0][i-1][0] + right[0][i-1], 'E']

    def calc_best_score(i, j):
            """
            Helper function to calculate the best out of all 3 possibilities of getting to node
            Returns:
                - Tuple of [score, direction]
                    score: best possible score for this node
                    direction: 'E', 'S', or 'D', indicating how we achieve that score
            Direction Tiebreaker: anti-clockwise, i.e. prioritise 'S', then 'D', then 'E'
            """
            e = [score_matrix[i][j-1][0] + right[i][j-1], 'E']
            s = [score_matrix[i-1][j][0] + down[i-1][j], 'S']
            d = [score_matrix[i-1][j-1][0] + diag[i-1][j-1], 'D'] if diag else [0, 'x']
            
            return max([e, s, d], key=lambda x: x[0]) # returns tuple with highest score

    for i in range(1, m): # for every row
        for j in range(1, n): # calculate every column
            score_matrix[i][j] = calc_best_score(i, j)

    if debug:
        print("Score matrix:")
        for row in score_matrix:
            print(row)

    return score_matrix

def print_path(score_matrix):
    m = len(score_matrix)
    n = len(score_matrix[0])
    path = ""

    # start at bottom right (final) node
    i = m-1
    j = n-1
    while score_matrix[i][j][1] != 'x': # starting node signified with 'x'
        path = score_matrix[i][j][1] + path # append direction to beginning of path
        # navigate to next node
        if score_matrix[i][j][1] == 'E': j-=1
        elif score_matrix[i][j][1] == 'S': i-=1
        elif score_matrix[i][j][1] == 'D': 
            i-=1
            j-=1
   
    print(path)
    
        

if __name__ == "__main__":
    main()