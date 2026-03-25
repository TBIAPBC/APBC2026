import argparse
import re

def read_data(filename): 
    with open (filename, 'r') as f:
        lines=f.readlines()
    
    municipality_cost=dict()
    parameters=re.findall(r"\d+", lines[0])
    city_list=re.findall(r"\w+", lines[1])
    
    number_of_cities=int(parameters[0])
    budget=int(parameters[1])
    
    idx = 2
    municipality_cost = {}
    minimum_additional_cost=number_of_cities//2-1

    while idx <= number_of_cities + 1:
        row = re.findall(r"-|\d+", lines[idx].strip())
        city_i = city_list[idx - 2]
        
        for city_j, cost in zip(city_list, row):
            if cost != "-":
                cost = int(cost) 
                if cost <= budget-minimum_additional_cost and city_i < city_j:
                    municipality_cost[(city_i, city_j)] = cost
        idx += 1 
    return (municipality_cost,city_list,budget)    

def find_pairings(unpaired_cities, municipality_cost, budget, current_pairs=None, current_cost=0):
    if current_pairs==None:
        current_pairs=[]
    if not unpaired_cities:
        return [current_pairs]  
    
    minimum_cost=min(municipality_cost.values())
    minimum_additional_cost=((len(unpaired_cities)//2)-1)*minimum_cost

    results=[]
    first_unpaired = unpaired_cities[0]

    for i in range(1, len(unpaired_cities)):
        second_unpaired = unpaired_cities[i]
        pair = (first_unpaired, second_unpaired)
        
        if pair in municipality_cost:
            new_cost = municipality_cost.get(pair)+current_cost
           
            if new_cost > budget - minimum_additional_cost:
                continue  
            
            new_remaining = unpaired_cities[1:i] + unpaired_cities[i+1:]

            results+=find_pairings(new_remaining, municipality_cost, budget, current_pairs + [pair], new_cost)
    return results        

def find_minimum(possible_municipalities, municipality_cost, budget):
    lowest_cost=budget
    cheapest_partition=[]
    for pairs in possible_municipalities:
        total_cost=0   
        for pair in pairs:
            cost=municipality_cost.get(pair)
            total_cost+=cost
        if total_cost<=lowest_cost:
            lowest_cost=total_cost
            cheapest_partition.append(pairs)
    return lowest_cost, cheapest_partition



if __name__=="__main__":
    
    parser = argparse.ArgumentParser(description='Lists all ways to partition the provinces within a specific budget')
    parser.add_argument('filename', type=str, help='The name of the file containing the adjacency matrix and budget limit.')
    parser.add_argument('-o', action="store_true", help="Prints the lowest total cost instead of a list of possible partitions")
    parser.add_argument('-op', action="store_true", help="Prints the lowest total cost and which partition/s are possible at such cost")
    args=parser.parse_args()

    
    data=read_data(args.filename)
    partitions = find_pairings(data[1], data[0], data[2])
    min_cost=find_minimum(partitions,data[0],data[2])
    if args.o:    
        print(f'Minimum partitioning cost = {min_cost[0]}')
    elif args.op:
        print(f'Minimum partitioning cost = {min_cost[0]}')
        print(f'Partitions possible at this cost:')
        for partition in min_cost[1]:
            for i in partition:
                print(f'{i[0]+i[1]} ', end="")
            print("")
    else:  
        for partition in partitions:
            for i in partition:
                print(f'{i[0]+i[1]} ', end="")     
            print("")  
            