import numpy as np
import argparse 

def read_matrices(filename):
    
    matrices = []
    matrix = []

    row_width = None 

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue
            
            row = []
            
            if line.startswith("#"):
                if len(matrix) > 0:
                    matrices.append(matrix)
                    matrix = []
                continue
            
            for x in line.split():
                if '.' in x:
                    decimals = x.split('.')[1]
                    if len(decimals) > 2:
                        return 0
                row.append(float(x))
            
            if row_width == None:
                row_width = len(row)
                
            elif row_width != len(row):
                if len(matrix) > 0:
                    matrices.append(matrix)
        
                matrix = []
                row_width = len(row)

            matrix.append(row)
            
        if len(matrix) > 0:
            matrices.append(matrix)

    if len(matrices) == 3:
        return matrices[0], matrices[1], matrices[2]
    
    elif len(matrices) == 2:
        return matrices[0], matrices[1]
    
    else:
        return 1 

def path_scoring(down, right, diag_moves):
    
    n=len(down)
    m=len(right[0])

    if len(diag_moves) == 0:
        d = False
    else:
        d = True
        
    grid = np.zeros((n+1,m+1))
    
    for i in range(1, n+1):
        grid[i][0] = grid[i-1][0] + down[i-1][0]
    
    for j in range (1, m+1):
        grid[0][j] = grid[0][j-1] + right[0][j-1]

    for i in range(1,n+1):
        for j in range(1,m+1):
            from_top = grid[i-1][j] + down[i-1][j]
            from_left = grid[i][j-1] + right[i][j-1]
            
            if d:
                from_diag = grid[i-1][j-1] + diag_moves[i-1][j-1]
                choice, _ = max([('S', from_top), ('E', from_left), ('D', from_diag)], key = lambda x: x[1])
                
            else:
                choice, _ = max([('S', from_top), ('E', from_left)], key = lambda x: x[1])
                
            if choice == 'S':
                grid[i][j] = from_top
                
            elif choice == 'E':
                grid[i][j] = from_left
              
            elif choice == 'D':
                grid[i][j] = from_diag
       
    fin_path = backtrack(grid, down, right, diag_moves, d)  
    max_score = grid[n][m]  

    return max_score, fin_path

def backtrack(grid, down, right, diag, d):

        i = len(grid)-1
        j = len(grid[0])-1

        path = []

        while i > 0 or j > 0:
            
            if i == 0:
                path.append('E')
                j -= 1

            elif j == 0:
                path.append('S')
                i -= 1

            else:
                up = grid[i - 1][j] + down[i-1][j]
                left = grid[i][j - 1] + right[i][j-1]
                
                if d:
                    diagonal = grid[i -1][j - 1] + diag[i - 1][j - 1]
                    choice, _ = max([('S', up), ('E', left), ('D', diagonal)], key = lambda x: x[1])
                    
                else:
                    choice, _ = max([('S', up), ('E', left)], key = lambda x: x[1])
                    
                if choice == 'S':
                    path.append('S')
                    i -= 1
                    
                elif choice == 'E':
                    path.append('E')
                    j -= 1
                    
                else:  
                    path.append('D')
                    i -= 1
                    j -= 1

        fin_path=''.join(reversed(path))
    
        return fin_path
    
if __name__ == "__main__": 
    
    parser = argparse.ArgumentParser(description = 'Finds highest score of any path possible')
    parser.add_argument('filename', type = str, help = 'The name of the file containing the weights for every possible direction at every position. The script assumes the directions are ordered like this: down, left, diagonal (if applicable)')
    parser.add_argument('-t', action = 'store_true', help = 'Prints the path generating the highest score additionally to the score')
    parser.add_argument('-d', action = 'store_true', help = 'By default the script will only output paths based on down and right movements (even if your input file includes diagonal moves). To include diagonal moves you have to set -d')
    args=parser.parse_args()
    
    placeholder = []
    matrices = read_matrices(args.filename)
    
    if matrices == 0:
        print('Too many decimal places')
    
    if matrices == 1:
        print(f'Wrong Matrix Dimensions, {len(matrices)} Matrices found')
    
    else:
        down = np.array(matrices[0])
        right = np.array(matrices[1])

        if args.d and len(matrices) == 3: 
            diag = np.array(matrices[2])
            run_script = path_scoring(down, right, diag)
                 
        elif args.d and len(matrices) < 3:
            print('You chose -d but your input file does not seem to have the right amount of matrices. No diagonal moves were found and path was calculated using the up and right matrices available')
            run_script = path_scoring(down, right, placeholder)

        elif args.d == False and len(matrices) == 3:
            print('Your input file contains an additional matrix which might specify diagonal moves. These were not included in the calculation, if you want to include them please use -d.')
            run_script = path_scoring(down, right, placeholder)
            
        else:
            run_script = path_scoring(down, right, placeholder)
            
        score =  run_script[0]
        path = run_script[1]
        print(f'{score:.2f}')
        if args.t:
            print(path)