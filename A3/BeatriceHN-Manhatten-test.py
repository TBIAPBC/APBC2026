import numpy as np
import argparse


def file_structure(file):
    with open(file, 'r') as f:
        lines = f.readlines()

    v_keys = ['down', 'north-south', 'n-s', 'vertical', 'v']
    h_keys = ['right', 'west-east', 'w-e', 'horizontal', 'h']
    d_keys = ['diag', 'diagonal', 'd']
    
    # Check if the file has any descriptive labels
    all_keys = v_keys + h_keys + d_keys + ['size']
    has_headers = any(k in line.lower() for line in lines for k in all_keys)

    if has_headers:
        return parse_by_keys(lines, v_keys, h_keys, d_keys)
    else:
        return parse_plain(lines)

def parse_by_keys(file, v_keys, h_keys, d_keys):
    key_map = {
        'v': v_keys,
        'h': h_keys,
        'd': d_keys
    }
    
    sections = {'v': [], 'h': [], 'd': []}
    current_key = None
    
    for line in file:
        clean = line.strip()
        if not clean:
            continue
            
        lower_line = clean.lower()
        
        # 1. Check if the line is a header
        found_header = False
        for section_id, keywords in key_map.items():
            if any(k in lower_line for k in keywords):
                current_key = section_id
                found_header = True
                break
        
        # 2. Handle the line logic
        if found_header:
            continue
        elif clean.startswith('#'):
            continue
        elif current_key:
            sections[current_key].append(list(map(float, clean.split())))
            
    down = np.array(sections['v'])
    right = np.array(sections['h'])
    diag = np.array(sections['d']) if sections['d'] else None
    
    r, c = down.shape[0], down.shape[1] - 1
    return r, c, down, right, diag

def parse_plain(file):
    data_rows = []
    for line in file:
        clean = line.strip()
        if clean:
            nums = list(map(float, clean.split()))
            data_rows.append(nums)

    first_col_count = len(data_rows[0])
    split_index = -1
    
    for i in range(len(data_rows)):
        if len(data_rows[i]) != first_col_count:
            split_index = i
            break

    v_data = data_rows[:split_index]
    h_data = data_rows[split_index:]
    
    down = np.array(v_data)
    right = np.array(h_data)
    
    n = down.shape[0]
    m = down.shape[1] - 1
    
    diag = None
    
    return n, m, down, right, diag

def manhatten_tour(n, m, down, right, diag=None):
    score_matrix = np.zeros((n + 1, m + 1))
    choices = np.zeros((n + 1, m + 1), dtype=int) 
    
    # Fill boundaries
    for i in range(1, n + 1):
        score_matrix[i, 0] = score_matrix[i-1, 0] + down[i-1, 0]
        choices[i, 0] = 1 
    for j in range(1, m + 1):
        score_matrix[0, j] = score_matrix[0, j-1] + right[0, j-1]
        choices[0, j] = 2 
    
    # Fill DP table
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            opt_s = score_matrix[i-1, j] + down[i-1, j]
            opt_e = score_matrix[i, j-1] + right[i, j-1]
            
            if diag is not None:
                opt_d = score_matrix[i-1, j-1] + diag[i-1, j-1]
                # Tie-breaker: South (index 0) > East (index 1) > Diagonal (index 2)
                options = [opt_s, opt_e, opt_d]
                best_val = max(options)
                score_matrix[i, j] = best_val
                choices[i, j] = options.index(best_val) + 1
            else:
                if opt_s >= opt_e: # Explicit South preference
                    score_matrix[i, j] = opt_s
                    choices[i, j] = 1
                else:
                    score_matrix[i, j] = opt_e
                    choices[i, j] = 2
                    
    return score_matrix[n, m], choices

def get_path(n, m, choices):
    path = []
    i, j = n, m
    while i > 0 or j > 0:
        if choices[i, j] == 1: # South
            path.append('S')
            i -= 1
        elif choices[i, j] == 2: # East
            path.append('E')
            j -= 1
        else: # Diagonal
            path.append('D')
            i -= 1
            j -= 1
    return ''.join(reversed(path))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Manhattan Tourist Problem.')
    
    parser.add_argument('filename', help='Path to the input file')
    
    parser.add_argument('-d', action='store_true', help='Consider diagonal edges')
    parser.add_argument('-t', action='store_true', help='Print the best path (traceback)')

    args = parser.parse_args()

    n, m, down, right, diag = file_structure(args.filename)

    max_weight, choices = manhatten_tour(n, m, down, right, diag=diag)
    print(max_weight)
    if args.t:
        best_path = get_path(n, m, choices)
        print(best_path)

    
