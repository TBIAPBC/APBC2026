import argparse
import sys

# defining arguments
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs = "?")
    parser.add_argument("-d", action="store_true", help = "Additionally process input files with diagonals.")
    parser.add_argument("-t", action="store_true", help = "Prints weight of the maximum path and the corresponding best path.")
    parser.add_argument("-f", action="store_true", help = "I wonder what this does...")
    parser.add_argument("--out", help = "Defines the output file [OUTPUT.out]")
    

    args = parser.parse_args()


    # if the --out argument is used, the output will be writen to a file
    if args.out:
        out = open(args.out, "w")
    else:
        out = sys.stdout # if --out is not used, the result will be printed to the terminal


    #open the given file / STDIN also possible ( < )
    if args.filename:
        with open(args.filename) as r:
            matrix_text = r.read()
    else:
        if sys.stdin.isatty():
            raise ValueError("No input provided. Please specify an input file or use STDIN.")
        matrix_text = sys.stdin.read()



    def parse_hv(matrix_text):
        lines = []
        for raw_line in matrix_text.splitlines():
            line = raw_line.split("#", 1)[0].strip() 
            if line:
                lines.append(line)
        
        if not lines:
            raise ValueError("?..... The Input File is ... empty!?")
        
        try:
            rows = [list(map(float, line.split())) for line in lines]
        except ValueError:
            raise ValueError("Input contains non-numeric values.")

        # splits the input in two blocks. (down / north-south) (right/ west-east)
        split_index = None

        for k in range(1, len(rows)):
            down = rows[:k]
            right = rows[k:]

            down_widths = {len(row) for row in down}
            right_widths = {len(row) for row in right}

            if len(down_widths) == 1 and len(right_widths) == 1:
                down_w = len(down[0])
                right_w = len(right[0])

                if down_w == right_w + 1 and len(right) == len(down) + 1:
                    split_index = k # k is where we want to split the input
                    break
        
        if split_index is None:
            raise ValueError("Invalid HV input format.")

        down = rows[:split_index]
        right = rows[split_index:]

        if len(down[0]) != len(right[0]) + 1:
            raise ValueError("Invalid matrix dimensions.")

        return down, right


    def parse_hvd(matrix_text):
        down = []
        right = []
        diag = []

        current_block = None

        for raw_line in matrix_text.splitlines():
            line = raw_line.strip()

            if not line:
                continue

            if line.startswith("#"):
                if line.startswith("#G_down"):
                    current_block = "down"
                elif line.startswith("#G_right"):
                    current_block = "right"
                elif line.startswith("#G_diag"):
                    current_block = "diag"
                elif line.startswith("#---"):
                    continue
                else:
                    continue

            else:
                try:
                    row = list(map(float, line.split()))
                except ValueError:
                    raise ValueError("Input contains non-numeric values.")

                if current_block == "down":
                    down.append(row)
                elif current_block == "right":
                    right.append(row)
                elif current_block == "diag":
                    diag.append(row)
                else:
                    raise ValueError("Found matrix row before block label.")

        if not down or not right or not diag:
            raise ValueError("Invalid HVD input format.")

        if len({len(row) for row in down}) != 1:
            raise ValueError("Invalid HVD input: rows in the down matrix have different lengths.")

        if len({len(row) for row in right}) != 1:
            raise ValueError("Invalid HVD input: rows in the right matrix have different lengths.")

        if len({len(row) for row in diag}) != 1:
            raise ValueError("Invalid HVD input: rows in the diagonal matrix have different lengths.")

        if len(right) != len(down) + 1:
            raise ValueError(
                f"Invalid HVD input: the right matrix has {len(right)} rows, "
                f"but it should have exactly one more row than the down matrix ({len(down)} rows)."
            )

        if len(diag) != len(down):
            raise ValueError(
                f"Invalid HVD input: the diagonal matrix has {len(diag)} rows, "
                f"but it should have the same number of rows as the down matrix ({len(down)} rows)."
            )

        if len(down[0]) != len(right[0]) + 1:
            raise ValueError(
                f"Invalid HVD input: the down matrix has {len(down[0])} columns, "
                f"but it should have exactly one more column than the right matrix ({len(right[0])} columns)."
            )

        if len(diag[0]) != len(right[0]):
            raise ValueError(
                f"Invalid HVD input: the diagonal matrix has {len(diag[0])} columns, "
                f"but it should have the same number of columns as the right matrix ({len(right[0])} columns)."
            )

        return down, right, diag



    def manhattan_hv(down, right):
        n = len(down)
        m = len(right[0])

        score = [[0.0] * (m + 1) for _ in range(n + 1)]
        backtrack = [[""] * (m + 1) for _ in range(n + 1)]

        # fill first column
        for i in range(1, n + 1):
            score[i][0] = score[i - 1][0] + down[i - 1][0]
            backtrack[i][0] = "S"

        # fill first row
        for j in range(1, m + 1):
            score[0][j] = score[0][j - 1] + right[0][j - 1]
            backtrack[0][j] = "E"

        # fill the rest of the matrix
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                from_up = score[i - 1][j] + down[i - 1][j]
                from_left = score[i][j - 1] + right[i][j - 1]

                if from_up >= from_left:   # tie -> prefer south
                    score[i][j] = from_up
                    backtrack[i][j] = "S"
                else:
                    score[i][j] = from_left
                    backtrack[i][j] = "E"

        return score, backtrack
        

    def manhattan_hvd(down, right, diag):
        n = len(down)
        m = len(right[0])

        score = [[0.0] * (m + 1) for _ in range(n + 1)]
        backtrack = [[""] * (m + 1) for _ in range(n + 1)]

        for i in range(1, n + 1):
            score[i][0] = score[i - 1][0] + down[i - 1][0]
            backtrack[i][0] = "S"

        for j in range(1, m + 1):
            score[0][j] = score[0][j - 1] + right[0][j - 1]
            backtrack[0][j] = "E"

        for i in range(1, n + 1):
            for j in range(1, m + 1):
                from_up = score[i - 1][j] + down[i - 1][j]
                from_left = score[i][j - 1] + right[i][j - 1]
                from_diag = score[i - 1][j - 1] + diag[i - 1][j - 1]

                best = max(from_up, from_left, from_diag)

                if from_up == best:          
                    score[i][j] = from_up
                    backtrack[i][j] = "S"
                elif from_left == best:
                    score[i][j] = from_left
                    backtrack[i][j] = "E"
                else:
                    score[i][j] = from_diag
                    backtrack[i][j] = "D"

        return score, backtrack


    def traceback_hv(backtrack):
        i = len(backtrack) - 1
        j = len(backtrack[0]) - 1
        path = []

        while i > 0 or j > 0:
            move = backtrack[i][j]
            path.append(move)

            if move == "S":
                i -= 1
            elif move == "E":
                j -= 1
            else:
                raise ValueError("Invalid traceback matrix.")

        path.reverse()
        return "".join(path)


    def traceback_hvd(backtrack):
        i = len(backtrack) - 1
        j = len(backtrack[0]) - 1
        path = []

        while i > 0 or j > 0:
            move = backtrack[i][j]
            path.append(move)

            if move == "S":
                i -= 1
            elif move == "E":
                j -= 1
            elif move == "D":
                i -= 1
                j -= 1
            else:
                raise ValueError("Invalid traceback matrix.")

        path.reverse()
        return "".join(path)




    if args.d:
        down, right, diag = parse_hvd(matrix_text)
        score, backtrack = manhattan_hvd(down, right, diag)
        result = score[-1][-1]
    else:
        down, right = parse_hv(matrix_text)
        score, backtrack = manhattan_hv(down, right)
        result = score[-1][-1]
    


    if result.is_integer():
        print(int(result), file=out)
    else:
        print(f"{result:.2f}", file=out)

    if args.t:
        if args.d:
            path = traceback_hvd(backtrack)
        else:
            path = traceback_hv(backtrack)
        print(path, file=out)


    if args.out:
        out.close()























































































    # Hidden fun fact.
    if args.f:
        print(
            "\nFun Fact!\n"
            "At one point in Manhattan, the law basically said: no drinking without food. "
            "So bars responded by keeping one horrible token sandwich around as a legal loophole "
            "and serving alcohol anyway."
        )
    # https://www.atlasobscura.com/articles/raines-sandwich?utm_source=chatgpt.com


if __name__ == "__main__":
    main()