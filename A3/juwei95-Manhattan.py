import argparse
from dataclasses import dataclass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog='juwei95-Manhattan.py', description='Find the best path through a grid.')
    parser.add_argument('filename')
    parser.add_argument('-t', '--trace',    action='store_true', help='print the best path')
    parser.add_argument('-d', '--diagonal', action='store_true', help='allow diagonal edge weights')
    return parser.parse_args()

Edges = list[list[float]]
def parse_matrix(args: argparse.Namespace) -> tuple[Edges, Edges, Edges]:
    down, right, diagonal = [], [], []
    with open(args.filename) as f:
        for line in f:
            if '#' in line:
                hashpos = line.find('#')
                line = line[:hashpos]
            if line.isspace() or '' == line:
                continue
            weights = []
            for weight in line.split():
                weights.append(float(weight))
            if len(down) == 0 or len(weights) == len(down[-1]):
                down.append(weights)
            elif len(right) == 0 or len(right) != len(down) + 1:
                right.append(weights)
            else:
                diagonal.append(weights)
    return down, right, diagonal
            
@dataclass
class Node:
    score:           float
    previous_row:    int
    previous_column: int
    row:             int
    column:          int

    def direction(self):
        if self.previous_row < self.row and self.previous_column < self.column:
            return 'D'
        if self.previous_row < self.row:
            return 'S'
        if self.previous_column < self.column:
            return 'E'
        
Grid = list[list[Node]]
def initialize_grid(down: Edges, right: Edges) -> Grid:
    memo   = []
    n      = len(right)
    m      = len(down[0])
    for i in range(n):
        row = []
        for j in range(m):
            row.append(Node(0, -1, -1, i, j))
        memo.append(row)
    return memo

def find_path(memo: Grid, start_node: Node, down: Edges, right: Edges, diagonal: Edges, args: argparse.Namespace):
    n      = len(right)
    m      = len(down[0])
    queue  = [start_node]
    while len(queue) > 0:
        current = queue.pop(0)
        for edges in [right, down, diagonal]:
            new_score = 0
            next_node = None
            if edges is right and current.column + 1 < m:
                next_node = memo[current.row][current.column + 1]
            if edges is down and current.row + 1 < n:
                next_node = memo[current.row + 1][current.column]
            if edges is diagonal and args.diagonal and current.row + 1 < n and current.column + 1 < m:
                next_node = memo[current.row + 1][current.column + 1]
            if next_node is not None:
                new_score = edges[current.row][current.column] + current.score
                if new_score > next_node.score:
                    next_node.score = new_score
                    next_node.previous_row = current.row
                    next_node.previous_column = current.column
                    queue.append(next_node)

def traceback(end_node: Node, memo: Grid, args: argparse.Namespace) -> list[Node]:
    if args.trace:
        path = [end_node]
        while end_node.previous_row >= 0 and end_node.previous_column >= 0:
            previous_node = memo[end_node.previous_row][end_node.previous_column]
            path.append(previous_node)
            end_node = previous_node
    return path

def main():
    args = parse_args()
    down, right, diagonal = parse_matrix(args)
    memo = initialize_grid(down, right)
    start_node = memo [0][0]
    end_node = memo [-1][-1]
    find_path(memo, start_node, down, right, diagonal, args)
    
    if int(end_node.score) == float(end_node.score):
        print(int(end_node.score))
    else:
        print("%.2f" % end_node.score)

    if args.trace:
        path = traceback(end_node, memo, args)
        path.reverse()
        path_str = ''.join(map(Node.direction, path[1:]))
        print(path_str)
   

if __name__ == '__main__':
    main()
    