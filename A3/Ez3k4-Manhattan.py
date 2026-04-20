import argparse
import re

def read_file(path):
    """
    Reads Manhattan input, ignores comments/empty lines,
    and splits numeric rows into down/right/(optional) diagonal by row width.
    """
    first_width = None
    down_weights = []
    right_weights = []
    diagonal_weights = []
    section = "down"  # down -> right -> diag

    with open(path, "rt", encoding="utf-8") as fh:
        for raw_line in fh:
            content = raw_line.split("#", 1)[0].strip()  # handles inline comments too
            if not content:
                continue

            
            pattern = re.compile(r"^-?\d+(?:[.,]\d{1,2})?$")

            values = []
            for x in content.split():
                if not pattern.match(x):
                    raise ValueError(f"Invalid number format: {x}")
                values.append(float(x.replace(",", ".")))
                        

            if first_width is None:
                first_width = len(values)

            if section == "down":
                if len(values) == first_width:
                    down_weights.append(values)
                    expected_right_rows = len(down_weights) + 1
                else:
                    section = "right"
                    right_weights.append(values)

            elif section == "right":
                right_weights.append(values)
                if expected_right_rows is not None and len(right_weights) >= expected_right_rows:
                    section = "diag"

            else:
                diagonal_weights.append(values)

    if not down_weights or not right_weights:
        raise ValueError("Could not parse down/right matrices from input.")

    diag = diagonal_weights if diagonal_weights else None
    return down_weights, right_weights, diag

def dp_matrix(down_weights, right_weigths, use_diagonal=False, diagonal_weights=None):
    # build initial frame
    dp_mtx = []
    # produce first row
    row_cost = 0
    first_row = [float(0)]
    for n in right_weigths[0]:
        row_cost += n
        first_row.append(row_cost)
    dp_mtx.append(first_row)

    # produce first col
    col_cost = 0
    first_col = [float(0)]
    for col in down_weights:
        col_cost += col[0]
        first_col.append(col_cost)
    for n in range(1, len(first_col)):
        dp_mtx.append([first_col[n]])


    # start to fill inner interior
    for r in range(1, len(dp_mtx)):
        for c in range(1, len(dp_mtx[0])):

            walk_down = down_weights[r-1][c]
            walk_left = right_weigths[r][c-1]
            upper = dp_mtx[r-1][c]
            left = dp_mtx[r][c-1]

            if use_diagonal and diagonal_weights is None:
                raise ValueError("No diagonal values found")
            
            if use_diagonal:
                walk_diagonal = diagonal_weights[r-1][c-1]
                diagonal = dp_mtx[r-1][c-1]
                new_value = max((left + walk_left), (upper + walk_down), (diagonal + walk_diagonal))
                dp_mtx[r].append(new_value)

            else:
                new_value = max((left + walk_left), (upper + walk_down))
                dp_mtx[r].append(new_value)

    path = traceback(dp_mtx, down_weights, right_weigths, use_diagonal, diagonal_weights)
    return dp_mtx[-1][-1] , path

def traceback(dp_mtx, down_weights, right_weights, use_diagonal=False, diagonal_weights=None):
    x = len(dp_mtx[0]) - 1
    y = len(dp_mtx) - 1

    path = []

    while x > 0 or y > 0:
        # Border cases: only one legal move
        if x == 0:
            path.append("S")
            y -= 1
            continue

        if y == 0:
            path.append("E")
            x -= 1
            continue

        # Interior: compare full predecessor scores
        from_top = dp_mtx[y - 1][x] + down_weights[y - 1][x]
        from_left = dp_mtx[y][x - 1] + right_weights[y][x - 1]

        if use_diagonal:
            from_diagonal = dp_mtx[y - 1][x - 1] + diagonal_weights[y-1][x-1]

            if from_top >= from_left and from_top >= from_diagonal:  # prefer south on ties
                path.append("S")
                y -= 1
            elif from_diagonal >= from_left and from_diagonal > from_top: # prefer D because still more south than E
                path.append("D")
                x -= 1
                y -= 1
            else:
                path.append("E")
                x -= 1
        else:
            if from_top >= from_left:  # prefer south on ties
                path.append("S")
                y -= 1
            else:
                path.append("E")
                x -= 1

    return "".join(reversed(path))

def parse_args():
    parser = argparse.ArgumentParser(description="Solve Manhattan Tourist problem (HV or HVD).")
    parser.add_argument(
        "-d",
        action="store_true",
        dest="use_diagonal",
        help="Enable diagonal edges (HVD input).",
    )
    parser.add_argument(
        "-t",
        action="store_true",
        dest="print_trace",
        help="Print traceback path in addition to best score.",
    )
    parser.add_argument(
        "input_file",
        help="Path to input file.",
    )
    return parser.parse_args()


if __name__ == "__main__":

    args = parse_args()

    down_weights, right_weights, diagonal_weights = read_file(args.input_file)
    max_value, path = dp_matrix(down_weights, right_weights, use_diagonal=args.use_diagonal, diagonal_weights=diagonal_weights)
    print(max_value)

    if args.print_trace:
        print(path)
