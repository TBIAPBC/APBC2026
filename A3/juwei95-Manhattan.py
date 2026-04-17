# ignore comments in input
# args: testfile, -t, -d

import argparse
from dataclasses import dataclass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog='juwei95-Manhattan.py', description='Find the best path through a grid.')
    parser.add_argument('filename')
    parser.add_argument('-t', '--trace',    action='store_true', help='print the best path')
    parser.add_argument('-d', '--diagonal', action='store_true', help='allow diagonal edge weights')
    args = parser.parse_args()
    return args
    # print(args.filename, args.trace, args.diagonal)

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
            # print(line, end="")
    return down, right, diagonal
    # print(down)
    # print(right)
    # print(diagonal)
            
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

def find_path(memo, down, right, diagonal):
    n      = len(right)
    m      = len(down[0])
    queue = [memo[0][0]]
    while len(queue) > 0:
        current = queue.pop(0)
        if current.row + 1 < n:
            # print(current.row + 1, n)
            down_node = memo[current.row + 1][current.column]
            new_score = down[current.row][current.column] + current.score
            if new_score > down_node.score:
                down_node.score = new_score
                queue.append(down_node)
        if current.column + 1 < m:
            # print(current.column + 1, m)
            right_node = memo[current.row][current.column + 1]
            new_score = right[current.row][current.column] + current.score
            if new_score > right_node.score:
                right_node.score = new_score
                queue.append(right_node)
    end_node = memo [-1] [-1]
    return end_node

def main():
    args   = parse_args()
    down, right, diagonal = parse_matrix(args)
    memo = initialize_grid(down, right)
    end_node = find_path(memo, down, right, diagonal)

    # for i in memo:
    #     for j in i:
    #         print(j.score, end=' ')
    #         # print("%4.2f" % j.score, end=' ')
    #     print()

    if int(end_node.score) == float(end_node.score):
        print(int(end_node.score))
    else:
        print("%.2f" % end_node.score)





if __name__ == '__main__':
    main()