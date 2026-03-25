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

    while idx <= number_of_cities + 1:
        row = re.findall(r"-|\d+", lines[idx].strip())
        row_city = city_list[idx - 2]
        
        for col_city, cost in zip(city_list, row):
            if cost != "-":
                cost = int(cost)
                if cost < budget and row_city < col_city:
                    municipality_cost[(row_city, col_city)] = cost
        idx += 1
           
    return (municipality_cost,city_list,budget)    

def find_pairings(unpaired_cities, municipality_cost, budget, current_pairs=None, current_cost=0):
    if current_pairs==None:
        current_pairs=[]
    if not unpaired_cities:
        return [current_pairs]  
    else:
        opt_completion_cost=(len(unpaired_cities)//2)-1
     
    results=[]
    first_unpaired = unpaired_cities[0]

    for i in range(1, len(unpaired_cities)):
        second_unpaired = unpaired_cities[i]
        pair = (first_unpaired, second_unpaired)

        if pair in municipality_cost:
            cost = municipality_cost.get(pair)
            updated_cost=cost+current_cost+opt_completion_cost
            if updated_cost > budget:
                continue  
            
            new_remaining = unpaired_cities[1:i] + unpaired_cities[i+1:]
        
            results+=find_pairings(new_remaining,municipality_cost,budget,current_pairs + [pair],current_cost + cost)

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
    args=parser.parse_args()

    
    data=read_data(args.filename)
    partitions = find_pairings(data[1], data[0], data[2])
         
    if args.o:    
        min_cost=find_minimum(partitions,data[0],data[2])
        print(f'Minimum partitioning cost={min_cost[0]}')
        #for partition: {min_cost[1]}')  #finish this with another flag to print which partition/s are the cheapest.
    else:
        for partition in partitions:
            for i in partition:
                print(f'{i[0]+i[1]} ', end="")     
            print("")  