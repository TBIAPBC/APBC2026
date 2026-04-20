import sys


def read_file(filename, diagonal = False):
    
    input_data = []
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            #delete everything after '#'
            line = line.split("#")[0].strip()
            #save if it was not only a commentary line
            if line:
                input_data.append(line.split())
                
    #number of columns of the grid
    m = len(input_data[0])
    
    #find number of lines of the grid, using n-s has dimensions (n-1) x m and w-e n x (m-1)
    n = 1
    for row in input_data:
        if len(row)==m:
            n += 1
        else: break
    
    #weights for north-south streets, (n-1) x m
    north_south = [[0.0]*m for _ in range(n-1)]
    for i in range(n-1):
        for j in range(m):
            #exchange a comma with a point, so python can handle it correctly
            north_south[i][j] = float(input_data[i][j].replace(",", "."))
            
    #weights for west-east streets        
    west_east = [[0.0]*(m-1) for _ in range(n)]
    for i in range(n):
        for j in range(m-1):
            west_east[i][j] = float(input_data[i+n-1][j].replace(",", "."))
            
    diag_moves = []
    
    if diagonal:
        diag_moves = [[0.0]*(m-1) for _ in range (n-1)]
        for i in range(n-1):
            for j in range(m-1):
                diag_moves[i][j] = float(input_data[i+2*n-1][j].replace(",", "."))
    
    return n,m,north_south, west_east, diag_moves

#calculates the maximum weight to each point in the grid
def weighted_matrix(north_south, west_east, n, m, diag_moves = None, diagonal = False):
    A = [[0.0]*m for _ in range(n)]
    #initialize first column, as there is only one possible path
    for i in range(1,n):
        A[i][0] = A[i-1][0] + north_south[i-1][0]
    #initialize first row, as there is only one possible path
    for j in range(1,m):
        A[0][j] = A[0][j-1] + west_east[0][j-1]
    
    if not diagonal:
        #take max path either from the upper node + n-s or the left node + w-e
        for i in range(1,n):
            for j in range(1, m):
                A[i][j] = max(A[i-1][j] + north_south[i-1][j], A[i][j-1] + west_east[i][j-1])
    else:
        #consider also the upper left node + diag_move
        for i in range(1,n):
            for j in range(1, m):
                A[i][j] = max(A[i-1][j] + north_south[i-1][j], A[i][j-1] + west_east[i][j-1],  A[i-1][j-1] + diag_moves[i-1][j-1])
          
    return A

#get maximum number of sights
def get_number_of_sights(A):
    return A[-1][-1]

#traceback of path
def get_path(A, north_south, west_east, diag_moves, diagonal = False):
    n = len(A)
    m = len(A[0])
    
    path = ''
    
    if not diagonal:
        i = n-1
        j = m-1
        #stops if one reaches the margin of the grid/matrix
        while i > 0 and j > 0:
                #moved south if bigger or equal; abs for rounding errors
                if abs(A[i][j] - A[i-1][j] - north_south[i-1][j]) < 1e-9:
                    path = 'S' + path
                    i -= 1
                #moved east
                else:
                    path = 'E' + path
                    j -= 1
                    
        #doing the last moves along the margin if matrix is not squared
        while i > 0:
            path = 'S' + path
            i -= 1
        while j > 0:
            path = 'E' + path
            j -= 1
    
    #diagonal moves were possible as well
    else:
        i = n-1
        j = m-1
        while i > 0 and j > 0:
            if abs(A[i][j] - A[i-1][j] - north_south[i-1][j]) < 1e-9:
                path = 'S' + path
                i -= 1
            elif abs(A[i][j] - A[i][j-1] - west_east[i][j-1]) < 1e-9:
                path = 'E' + path
                j -= 1
            else:
                path = 'D' + path
                i -= 1
                j -= 1
                
        while i > 0:
            path = 'S' + path
            i -= 1
        while j > 0:
            path = 'E' + path
            j -= 1
     
        
    return path
            
        


if __name__ == "__main__":
    
    filename = None
    for arg in sys.argv[1:]:
        if not arg.startswith("-"):
            filename = arg
            break

    diagonal = "-d" in sys.argv
    show_path = "-t" in sys.argv   
                
                
    n,m,north_south, west_east, diag_moves = read_file(filename, diagonal)   
           
    A = weighted_matrix(north_south, west_east, n, m, diag_moves, diagonal)
    print("%.2f" % get_number_of_sights(A))
    
    if show_path:
        print(get_path(A, north_south, west_east, diag_moves, diagonal))
    
     
    