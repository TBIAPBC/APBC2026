import sys

def parse_number(s):

    try:
        v = float(s)
        return int(v) if v == int(v) else v
    
    except ValueError:
        raise ValueError(f"Cannot parse number: {s!r}")
    
"""
reads file and returns streets_ns, streets_we, streets_diag
supports different input formats: labeled (section headers) and unlabeld (1-3 blocks) input 
"""
def read_file(filename): 

    # map for sections to keywords in header comment 
    KEYWORDS = {
        "ns": ("north-south", "north_south", "g_down", "down"),
        "we": ("west-east", "west_east", "g_right", "right"),
        "diag": ("diag", "g_diag"),
    }

    # returns section name that matches the keyword in the header, or None
    def detect_section(header):
        t = header.lower() 
        return next((s for s, keys in KEYWORDS.items() if any (k in t for k in keys)), None)
    
    # strips comments and parses each token to a number
    def parse_row(line):
        return [parse_number(x) for x in line.split("#")[0].split()]
    

    sections = {"ns": [], "we": [], "diag": []} # stores rows that can be assigned a specific sections 
    blocks = [] # unlabeled groups of rows 
    current_block = [] 
    current_section = None

    for i in open(filename):
        line = i.strip()
        if not line: # end of current unlabeled block 
            if current_block: # add current block to blocks 
                blocks.append(current_block); current_block = []
        elif line.startswith("#"): # comment line 
            if current_block:
                blocks.append(current_block); current_block = []
            current_section = detect_section(line[1:]) or current_section # section keyword? else keep current section 
        else:
            row = parse_row(line) # parse data line 
            if row:
                (sections[current_section] if current_section else current_block).append(row) 
    
    if current_block: 
        blocks.append(current_block)

    if any(sections.values()): # labeled input => return sections 
        return sections["ns"], sections["we"], sections["diag"]
    
    if len(blocks) == 1: # one unlabeled block

        long = max(len(r) for r in blocks[0])
        ns   = [r for r in blocks[0] if len(r) == long]
        we   = [r for r in blocks[0] if len(r) != long]
        return ns, we, []

    if len(blocks) in (2, 3): # 2 blocks: (ns, we); 3 blocks: (ns, we, diag)
        return (*blocks[:3], [])[:3] if len(blocks) == 2 else tuple(blocks)
      
    
    raise ValueError("Unrecognised input format!") # unknown input format
    
"""
HV: horizontal and vertical moves only, no diagonal moves.
Uses dynamic programming to find best path from the top-left to 
the bottom.-right corner of the grid, here we maximise the weight of 
the path. 

streets_ns[i][j]  = weight of the south edge from (i,j) to (i+1,j)
streets_we[i][j]  = weight of the east edge from (i,j) to (i,j+1)
"""

def solve_hv(streets_ns, streets_we, traceback=False):
    
    # grid dimensions
    rows = len(streets_ns) + 1
    cols = len(streets_we[0]) + 1
 
    # weight stores best total weight of any path from (0,0) to (i,j)
    weight = [[float('-inf')] * cols for _ in range(rows)]
    weight[0][0] = 0.0 # start at 0.0
 
    # Initialise top row 
    for j in range(1, cols):
        weight[0][j] = weight[0][j-1] + streets_we[0][j-1]
 
    # Initialise left column 
    for i in range(1, rows):
        weight[i][0] = weight[i-1][0] + streets_ns[i-1][0]
 
    # Fill interior: to ways. from north or from west
    for i in range(1, rows):
        for j in range(1, cols):
            from_north = weight[i-1][j] + streets_ns[i-1][j]
            from_west  = weight[i][j-1] + streets_we[i][j-1]
            # take maximum of the two possible moves 
            weight[i][j] = max(from_north, from_west)
 
    # weight of best path 
    best = weight[rows-1][cols-1]
 
    if not traceback: # if -t option is not given, then only the best weight is needed and the best path is not returned 
        return best, None
 
    # Traceback the path 
    path = []
    i, j = rows - 1, cols - 1
    while i > 0 or j > 0:
        if i == 0:
            path.append('E')
            j -= 1
        elif j == 0:
            path.append('S')
            i -= 1
        else:
            from_north = weight[i-1][j] + streets_ns[i-1][j]
            from_west  = weight[i][j-1] + streets_we[i][j-1]
            # When weights are the same South is prefered 
            if from_north >= from_west:
                path.append('S')
                i -= 1
            else:
                path.append('E')
                j -= 1
 
    path.reverse() #path was collected backwards => has to be reversed
    return best, ''.join(path)
 
"""
HVD: horizontal, vertical and diagonal moves.
Same as HV but with diagonal moves.
Uses dynamic programming to find best path from the top-left to 
the bottom.-right corner of the grid, here we maximise the weight of 
the path. 

streets_ns[i][j]  = weight of the south edge from (i,j) to (i+1,j)
streets_we[i][j]  = weight of the east  edge from (i,j) to (i,j+1)
streets_diag[i][j] = weight of diagonal edge from (i,j) to (i+1,j+1)
"""

def solve_hvd(streets_ns, streets_we, streets_diag, traceback=False):
    
    
    # grid dimensions
    rows = len(streets_ns) + 1
    cols = len(streets_we[0]) + 1
 
    # weight stores best total weight of any path from (0,0) to (i,j)
    weight = [[float('-inf')] * cols for _ in range(rows)]
    weight[0][0] = 0.0 # start at 0.0
 
    # Initialise top row 
    for j in range(1, cols):
        weight[0][j] = weight[0][j-1] + streets_we[0][j-1]
 
    # Initialise left column 
    for i in range(1, rows):
        weight[i][0] = weight[i-1][0] + streets_ns[i-1][0]
 
    # Fill interior: to ways. from north or from west
    for i in range(1, rows):
        for j in range(1, cols):
            from_north = weight[i-1][j] + streets_ns[i-1][j]
            from_west  = weight[i][j-1] + streets_we[i][j-1]
            from_diag  = weight[i - 1][j - 1] + streets_diag[i - 1][j - 1]
            # take maximum of the two possible moves 
            weight[i][j] = max(from_north, from_west, from_diag)
 
    # weight of best path 
    best = weight[rows-1][cols-1]
 
    if not traceback: # if -t option is not given, then only the best weight is needed and the best path is not returned 
        return best, None
 
    # Traceback the path 
    path = []
    i, j = rows - 1, cols - 1
    while i > 0 or j > 0:
        if i == 0:
            path.append('E')
            j -= 1
        elif j == 0:
            path.append('S')
            i -= 1
        else:
            from_north = weight[i-1][j] + streets_ns[i-1][j]
            from_west  = weight[i][j-1] + streets_we[i][j-1]
            from_diag  = weight[i - 1][j - 1] + streets_diag[i - 1][j - 1]
            best_val = max(from_north, from_west, from_diag) 
            if from_north == best_val:  # prefer S
                path.append('S')
                i -= 1
            elif from_west == best_val: # then E
                path.append('E')
                j -= 1
            else: 
                path.append('D') # and last diagonal 
                i -= 1
                j -= 1
 
    path.reverse() #path was collected backwards => has to be reversed
    return best, ''.join(path)

 
# print integer if whole number, else 2 decimal places 
def format_score(score):

    if score == int(score):
        return str(int(score))
    return f"{score:.2f}"

 
def main():

    args = sys.argv[1:]
 
    if not args:
        sys.exit(1)
 
    diagonal  = '-d' in args # allow for diagonal moves 
    show_path = '-t' in args # print best path 
 
    file_args = [a for a in args if not a.startswith('-')]

    if not file_args:
        print("Error: no input file specified.", file=sys.stderr)
        sys.exit(1)

    filename = file_args[0]
    output_file = file_args[1] if len(file_args) > 1 else None
 
 
    streets_ns, streets_we, streets_diag = read_file(filename)
 
    if not streets_ns:
        print("Error: no north-south street data!", file=sys.stderr)
        sys.exit(1)
    if not streets_we:
        print("Error: no west-east street data!", file=sys.stderr)
        sys.exit(1)
 
    if diagonal:
        if not streets_diag:
            print("Error: -d given but no diagonal data!", file=sys.stderr)
            sys.exit(1)
        score, path = solve_hvd(streets_ns, streets_we, streets_diag, traceback=show_path)
    else:
        score, path = solve_hv(streets_ns, streets_we, traceback=show_path)
 
    lines = [format_score(score)]

    if show_path and path:
        lines.append(path)

    if output_file:
        with open(output_file, "w") as f:
            f.write("\n".join(lines) + "\n")
    else:
        for line in lines:
            print(line)
    
 
main()
    
    
           

    
