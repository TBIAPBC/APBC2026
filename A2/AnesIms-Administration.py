import argparse
import sys

# defining arguments
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs = "?")
    parser.add_argument("-o", action="store_true", help = "Prints the score of the best solution")
    parser.add_argument("-s", action="store_true", help = "Use in combination with -o, to see the solution(s) with the best score")
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
        matrix_text = sys.stdin.read()



    def parse_input(matrix_text):
        lines = []
        for raw_line in matrix_text.splitlines():
            line = raw_line.split("#", 1)[0].strip() # added this so i could add comments to the input files
            if line:
                lines.append(line)

        # safety checks for the input file
        if not lines:
            raise ValueError("The Input File is empty.")

        if len(lines) < 2:
            raise ValueError("Sorry, i cant work with that. The Input must contain at least a header line and a capitals line")
        
        first_line = lines[0].split()

        if len(first_line) != 2:
            raise ValueError("Header line must contain exactly two values: number of capitals and cost limit.")

        try:
            n_capitals = int(first_line[0])
            cost_limit = int(first_line[1])
        except ValueError:
            raise ValueError("Header values must be integers.")

        if n_capitals <= 0:
            raise ValueError("Number of capitals must be a positive integer.")

        if n_capitals % 2 != 0: # check for even number of capitals, oterwise we can not build pairs
            raise ValueError("Number of capitals must be even.")
        
        
        capitals = lines[1].split()

        if len(set(capitals)) != len(capitals):
            raise ValueError("Capital names must be unique.")

        if len(capitals) != n_capitals:
            raise ValueError("Hold up my friend: The number of capitals does not match the header")

        matrix_lines = lines[2:]

        if len(matrix_lines) != n_capitals:
            raise ValueError("Wait a minute: The number of matrix rows do not match the number of capitals")

        costs = {}

        for i, line in enumerate(matrix_lines):
            entries = line.split()

            if len(entries) != n_capitals:
                raise ValueError(f"Mhmm somethings wrong... The row {i} has wrong length")

            for j, value in enumerate(entries):
                if value == "-":
                    if i != j:
                        raise ValueError(f"Only diagonal entries may be '-'. But i foud that at row {i+1}, column {j+1}. ")
                    continue
                try:    
                    costs[(capitals[i], capitals[j])] = int(value)
                except ValueError:
                    raise ValueError(f"The matrix values must be integers or '-'. '{value}' at row {i+1}, column {j+1} looks off.")
        
        for a in capitals:
            for b in capitals:
                if a == b:
                    continue
                if costs[(a, b)] != costs[(b, a)]:
                    raise ValueError(f"The Matrix must be symmetric, but {a}-{b} and {b}-{a} differ.")

        return n_capitals, cost_limit, capitals, costs
    
    n_capitals, cost_limit, capitals, costs = parse_input(matrix_text)


    remaining = capitals.copy()
    current_cost = 0
    current_pairs = []
    solutions = []
    best_cost = cost_limit
    best_solutions = []    # for the -s argument
    found_solution = False

    def search(remaining, current_cost, current_pairs):
        nonlocal best_cost, found_solution, best_solutions

        if not remaining: # means we found a solution
            solution_str = " ".join(current_pairs)

            if args.o:
                if not found_solution or current_cost < best_cost:
                    found_solution = True
                    best_cost = current_cost
                    best_solutions = [solution_str]
                elif current_cost == best_cost:
                    best_solutions.append(solution_str)
            else:        
                solutions.append(solution_str)
            return        

        first = remaining[0]
        for i in range(1, len(remaining)):
            second = remaining[i]
            pair_cost = costs[(first, second)]
            new_cost = current_cost + pair_cost

            if args.o:
                if new_cost > best_cost:
                    continue
            else:
                if new_cost > cost_limit:
                    continue
        
            new_remaining = remaining[1:i] + remaining[i+1:]
            pair = first + second
            new_pairs = current_pairs + [pair]

            search(new_remaining, new_cost, new_pairs)
    
    search(remaining, current_cost, current_pairs)


    # print just the best cost to terminal/file if -o argument is used
    if args.o:
        if found_solution:
            print(best_cost, file = out)

            if args.s:
                for solution in best_solutions:
                    print(solution, file=out)

        else:
            print("Sad news.. There is no solution", file = out)
    else:    
        for solution in solutions:
            print(solution, file=out)


    if args.out:
        out.close()


if __name__ == "__main__":
    main()
