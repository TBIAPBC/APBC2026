import argparse
from dataclasses import dataclass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog='juwei95-Manhattan.py', description='Find the best path through a grid.')
    parser.add_argument('filename')
    parser.add_argument('-t', '--trace',    action='store_true', help='print the best path')
    parser.add_argument('-d', '--diagonal', action='store_true', help='allow diagonal edge weights')
    args = parser.parse_args()
    return args

def parse_matrix(args: argparse.Namespace): # typehint?
    down     = []
    right    = []
    diagonal = []
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
    score:  float
    trace:  str
    row:    int
    column: int

def initialize_grid(down, right):
    memo   = []
    n      = len(right)
    m      = len(down[0])
    for i in range(n):
        row = []
        for j in range(m):
            row.append(Node(0, '-', i, j))
        memo.append(row)
    return memo

def find_path(memo, down, right, diagonal, args):
    n      = len(right)
    m      = len(down[0])
    queue = [memo[0][0]]
    while len(queue) > 0:
        current = queue.pop(0)
        if current.column + 1 < m:
            right_node = memo[current.row][current.column + 1]
            new_score = right[current.row][current.column] + current.score
            if new_score > right_node.score:
                right_node.score = new_score
                right_node.trace = 'E' 
                queue.append(right_node)
        if current.row + 1 < n:
            down_node = memo[current.row + 1][current.column]
            new_score = down[current.row][current.column] + current.score
            if new_score > down_node.score:
                down_node.score = new_score
                down_node.trace = 'S'
                queue.append(down_node)
        if args.diagonal:
            if current.row + 1 < n and current.column + 1 < m:
                diagonal_node = memo[current.row + 1][current.column + 1]
                new_score = diagonal[current.row][current.column] + current.score
                if new_score > diagonal_node.score:
                    diagonal_node.score = new_score
                    diagonal_node.trace = 'D'
                    queue.append(diagonal_node)
    end_node = memo [-1][-1]
    return end_node

def traceback(end_node, memo, args):
    if args.trace:
        path = [end_node]
        while end_node.trace != '-':
            if end_node.trace == 'S':
                previous_node = memo[end_node.row - 1][end_node.column]
            if end_node.trace == 'E':
                previous_node = memo[end_node.row][end_node.column - 1]
            if end_node.trace == 'D':
                previous_node = memo[end_node.row - 1][end_node.column - 1]
            path.append(previous_node)
            end_node = previous_node
    return path

def main():
    args   = parse_args()
    down, right, diagonal = parse_matrix(args)
    memo = initialize_grid(down, right)
    end_node = find_path(memo, down, right, diagonal, args)
    
    if int(end_node.score) == float(end_node.score):
        print(int(end_node.score))
    else:
        print("%.2f" % end_node.score)

    if args.trace:
        path = traceback(end_node, memo, args)
        path.reverse()
        path_str = ''.join(map(lambda x: x.trace, path[1:]))
        print(path_str)
   

if __name__ == '__main__':
    main()