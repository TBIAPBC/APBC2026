def main():
    weights = read_weights(".\Manhattan-testHVD1.in", True)
    print_weights(weights[0], weights[1], weights[2])

def read_weights(filename, d):
    """
    Reads the input file for the Manhattan Tourist Problem.
        - comments are completely ignored
    Expects:
        - input file with 2 or 3 weight matrices
            - 3 if d, 2 if not
        - matrix North-South with dimensions n x m-1
        - matrix East-West with dimensions n-1 x m
        - matrix Diagonals with dimensions n-1 x m-1
        - weights have to be valid floating point numbers, invalid entries are ignored
    Returns:
        down: 2D list of north-south edge weights (m-1 rows x n columns)
        right: 2D list of east-west edge weights (m rows x n-1 columns)
        diag: 2D list of diagonal edge weights (m-1 rows x n-1 columns) (if d is set), else None
    """
    def parse_numbers(line):
        return [float(x.replace(',', '.')) for x in line.strip().split() if is_number(x)]

    # error handling for numbers
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
    print(n)
    # m = number of junction nodes north - south -> total number of input lines is either (m-1 + m) or (m-1 + m + m-1)
    if not d and (len(lines)+1)%2 != 0:
        raise Exception(f"Invalid Input: Number of rows for non-diagonal weight matrix has to follow format m-1 + m")
    elif d and (len(lines)+2)%3 != 0:
        raise Exception(f"Invalid Input: Number of rows for diagonal weight matrix has to follow format m-1 + m + m-1")
        
    m = int((len(lines) + 1)/2) if not d else int((len(lines) + 2)/3) 
    down = []
    for i in range(0, m-1):
        new_line = parse_numbers(lines[i])
        if len(new_line) != n:
            raise Exception(f"Expected {n} valid entries in north-south value matrix but found {len(new_line)} entries in line {i+1}")
        down.append(new_line) # m-1 entries
    
    right = []
    for i in range(m-1, 2*m - 1):
        new_line = parse_numbers(lines[i])
        if len(new_line) != n-1:
            raise Exception(f"Expected {n-1} valid entries in east-west value matrix but found {len(new_line)} entries in line {i+1}")
        right.append(new_line) # m entries
    
    if d:
        diag = []
        for i in range(2*m -1, 3*m -2):
            new_line = parse_numbers(lines[i])
            if len(new_line) != n-1:
                raise Exception(f"Expected {n-1} valid entries in diagonal value matrix but found {len(new_line)} entries in line {i+1}")
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

if __name__ == "__main__":
    main()