import numpy as np
import pandas as pd
import argparse

def get_administration(file):
    cost_df = pd.read_csv(file, skiprows=1, delimiter='\s+', na_values='-')
    cost_df.index = cost_df.columns
    cost_df = cost_df.astype(float)
    cost_df.values[np.tril_indices(len(cost_df))] = np.nan
    meta_df = pd.read_csv(file, nrows=1, header=None, delimiter='\s+')
    meta_df.columns = ['City_nr', 'Budget']
    return meta_df, cost_df

def get_valid_pairs(cost_df, budget):
    budget_mask = cost_df < budget
    cost_budget = cost_df[budget_mask]
    logic_mask = cost_df <= (budget-len(cost_df)/2)
    cost = cost_budget[logic_mask]
    result = cost.stack(0)

    valid_pairs = {}
    for city_1, city_2, cost in zip(result.index.get_level_values(0), result.index.get_level_values(1), result.values):
        if city_1 not in valid_pairs:
            valid_pairs[city_1] = []
        valid_pairs[city_1].append((city_2, cost))
        
    print(result)
    print(valid_pairs.items())

    return valid_pairs

def get_all_paths(valid_pairs):
    pass



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=argparse.FileType('r', encoding='utf-8'), help='File with number of capitals, total budget and  matrix for cost of partition')
    args = parser.parse_args()
    meta_df, cost_df = get_administration(args.file.name)
    print(f'{cost_df}\n{meta_df}')
    valid_pairs = get_valid_pairs(cost_df, meta_df['Budget'][0])
