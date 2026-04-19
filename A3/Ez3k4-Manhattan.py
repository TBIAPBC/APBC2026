


def read_file(file):
    """ 
    Reads file, ignores all comments and turns strings into floats with max 2 digits after comma
    It assumes that columns are always first in the list
      """
    num = None
    rows = []
    columns = []
    with open(file, "rt") as fh:
        for line in fh:
            line = line.strip()
            if line:
                if not line.startswith("#"):
                    line = line.split()
                    line = [float(x) for x in line] # add condition for max 2 digits after .
                    if num is None:
                        num = len(line)
                    if len(line) == num:
                        columns.append(line)
                    if len(line) != num:
                        rows.append(line)
    print("rows: ",rows)
    print("cols: ",columns)
    return rows, columns

def dp_matrix(cols, rows):
    # build initial frame
    dp_mtx = []
    # produce first row
    row_cost = 0
    first_row = [float(0)]
    for n in rows[0]:
        row_cost += n
        first_row.append(row_cost)
    dp_mtx.append(first_row)

    # produce first col
    col_cost = 0
    first_col = [float(0)]
    for col in cols:
        col_cost += col[0]
        first_col.append(col_cost)
    for n in range(1, len(first_col)):
        dp_mtx.append([first_col[n]])

    # start to fill inner interior
    for r in range(1, len(dp_mtx)):
        for c in range(1, len(dp_mtx[0])):

            walk_down = cols[r-1][c]
            walk_left = rows[r][c-1]
            print(walk_down)

            if "-d":
                walk_diagonal = 0

            upper = dp_mtx[r-1][c]
            print("upper:",upper)
            left = dp_mtx[r][c-1]
            print("left:",left)
            new_value = max((left + walk_left), (upper + walk_down))
            dp_mtx[r].append(new_value)
            print(dp_mtx)

    return dp_mtx[-1][-1]

file = "Manhattan-testHV1.in"
rows, cols = read_file(file)
print(dp_matrix(cols, rows))
