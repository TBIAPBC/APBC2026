import numpy as np
import pandas as pd
import argparse

def get_administration(file):
    cost_df = pd.read_csv(file, skiprows=1, delimiter=r'\s+', na_values='-')
    cost_df.index = cost_df.columns
    cost_df = cost_df.astype(float)
    mask = np.tril(np.ones(cost_df.shape)).astype(bool)
    cost_df = cost_df.where(~mask)
    meta_df = pd.read_csv(file, nrows=1, header=None, delimiter=r'\s+')
    meta_df.columns = ['City_nr', 'Budget']
    return meta_df, cost_df, cost_df.columns.tolist()

def get_valid_pairs(cost_df, budget):
    logic_mask = (cost_df < budget) & (cost_df <= (budget - ((len(cost_df)/2)-1)))
    result = cost_df[logic_mask].stack().dropna()

    valid_pairs = {}
    for city_1, city_2, cost in zip(result.index.get_level_values(0), result.index.get_level_values(1), result.values):
        if city_1 not in valid_pairs:
            valid_pairs[city_1] = []
        valid_pairs[city_1].append((city_2, cost))
    return valid_pairs

def get_all_paths(valid_pairs, budget, cities, visited=None, bill=0, current_path=None, tracks=None):
    if visited is None:
        visited = set()

    if current_path is None:
        current_path = []

    if tracks is None:
        tracks = []

    city_1 = None
    for city in cities:
        if city not in visited:
            city_1 = city
            break

    if city_1 is None:
        tracks.append((current_path.copy(), bill))
        return tracks

    visited.add(city_1)

    for city_2, cost in valid_pairs.get(city_1, []):
        if city_2 in visited:
            continue
        if bill + cost <= budget:
            visited.add(city_2)
            current_path.append((city_1 + city_2))
            get_all_paths(valid_pairs, budget, cities, visited, bill + cost, current_path, tracks)
            current_path.pop()
            visited.remove(city_2)

    visited.remove(city_1)

    return tracks

def display_output(tracks, optimization=False):
        if optimization:
            min_bill = min(tracks, key=lambda x: x[1])[1]
            opt_track = [t for t in tracks if t[1] == min_bill]
            for cities, bill in opt_track:
                print(' '.join(cities), bill)
        else:
            for cities, bill in tracks:
                print(' '.join(cities))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=argparse.FileType('r', encoding='utf-8'),
                         help='File with number of capitals, total budget and  matrix for cost of partition')
    parser.add_argument('-o', '--optimization', action='store_true')
    args = parser.parse_args()
    meta_df, cost_df, cities = get_administration(args.file.name)
    valid_pairs = get_valid_pairs(cost_df, meta_df['Budget'][0])
    tracks = get_all_paths(valid_pairs, meta_df['Budget'][0], cities)
    display_output(tracks, optimization=args.optimization)
