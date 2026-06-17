#include <algorithm>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <queue>
#include <cstdlib>
#include <iomanip>

struct Args {
    std::string filename;
    bool trace = false;
    bool diagonal = false;
};

Args parse_args(int argc, char* argv[]) {
    Args args;
    if (argc < 2) {
        std::cerr << "Usage: juwei95-Manhattan <filename> [-t|--trace] [-d|--diagonal]\n";
        std::exit(1);
    }

    args.filename = argv[1];
    for (int i = 2; i < argc; ++i) {
        std::string arg = argv[i];
        if (arg == "-t" || arg == "--trace") {
            args.trace = true;
        } else if (arg == "-d" || arg == "--diagonal") {
            args.diagonal = true;
        }
    }
    return args;
}

using Edges = std::vector<std::vector<double>>;

void parse_matrix(const Args& args, Edges& down, Edges& right, Edges& diagonal) {
    std::ifstream file(args.filename);
    if (!file) {
        std::cerr << "Error: cannot open file " << args.filename << "\n";
        std::exit(1);
    }

    std::string line;
    while (std::getline(file, line)) {
        // Remove comments
        auto pos = line.find('#');
        if (pos != std::string::npos) {
            line = line.substr(0, pos);
        }

        std::istringstream iss(line);
        std::vector<double> weights;
        double w;
        while (iss >> w) {
            weights.push_back(w);
        }

        if (weights.empty()) continue;

        if (down.empty() || weights.size() == down.back().size()) {
            down.push_back(weights);
        } else if (right.empty() || right.size() != down.size() + 1) {
            right.push_back(weights);
        } else {
            diagonal.push_back(weights);
        }
    }

    if (args.diagonal && diagonal.empty()) {
        std::cerr << "Error: -d specified but no diagonal edges found in input.\n";
        std::exit(-1);
    }
}

struct Node {
    double score = 0.0;
    int previous_row = -1;
    int previous_column = -1;
    int row = 0;
    int column = 0;

    char direction() const {
        if (previous_row < row && previous_column < column) return 'D';
        if (previous_row < row) return 'S';
        if (previous_column < column) return 'E';
        return '?';
    }
};

using Grid = std::vector<std::vector<Node>>;

Grid initialize_grid(const Edges& down, const Edges& right) {
    int n = right.size();
    int m = down[0].size();

    Grid memo(n, std::vector<Node>(m));
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < m; ++j) {
            memo[i][j] = Node{0.0, -1, -1, i, j};
        }
    }
    return memo;
}

void find_path(Grid& memo, Node& start_node,
               const Edges& down, const Edges& right,
               const Edges& diagonal, const Args& args) {

    int n = right.size();
    int m = down[0].size();

    std::queue<Node*> q;
    q.push(&start_node);

    while (!q.empty()) {
        Node* current = q.front();
        q.pop();

        // Right
        if (current->column + 1 < m) {
            Node& next = memo[current->row][current->column + 1];
            double new_score = right[current->row][current->column] + current->score;
            if (new_score > next.score) {
                next.score = new_score;
                next.previous_row = current->row;
                next.previous_column = current->column;
                q.push(&next);
            }
        }

        // Down
        if (current->row + 1 < n) {
            Node& next = memo[current->row + 1][current->column];
            double new_score = down[current->row][current->column] + current->score;
            if (new_score > next.score) {
                next.score = new_score;
                next.previous_row = current->row;
                next.previous_column = current->column;
                q.push(&next);
            }
        }

        // Diagonal
        if (args.diagonal &&
            current->row + 1 < n &&
            current->column + 1 < m) {

            Node& next = memo[current->row + 1][current->column + 1];
            double new_score = diagonal[current->row][current->column] + current->score;
            if (new_score > next.score) {
                next.score = new_score;
                next.previous_row = current->row;
                next.previous_column = current->column;
                q.push(&next);
            }
        }
    }
}

std::vector<Node*> traceback(Node* end_node, Grid& memo, const Args& args) {
    std::vector<Node*> path;
    if (args.trace) {
        Node* current = end_node;
        path.push_back(current);

        while (current->previous_row >= 0 && current->previous_column >= 0) {
            current = &memo[current->previous_row][current->previous_column];
            path.push_back(current);
        }
    }
    return path;
}

int main(int argc, char* argv[]) {
    Args args = parse_args(argc, argv);

    Edges down, right, diagonal;
    parse_matrix(args, down, right, diagonal);

    Grid memo = initialize_grid(down, right);

    Node& start_node = memo[0][0];
    Node& end_node = memo.back().back();

    find_path(memo, start_node, down, right, diagonal, args);

    if ((int)end_node.score == end_node.score) {
        std::cout << (int)end_node.score << "\n";
    } else {
        std::cout << std::fixed << std::setprecision(2) << end_node.score << "\n";
    }

    if (args.trace) {
        auto path = traceback(&end_node, memo, args);
        std::reverse(path.begin(), path.end());

        std::string path_str;
        for (size_t i = 1; i < path.size(); ++i) {
            path_str += path[i]->direction();
        }
        std::cout << path_str << "\n";
    }

    return 0;
}
