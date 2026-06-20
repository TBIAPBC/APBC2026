# Municipality Optimization – City Pairing
# Overview

This project optimizes the formation of municipalities (clusters of 2 cities) based on a cost matrix.

Each cluster has an associated cost.
The total cost of a partition must not exceed a specified budget.
The script can either list all valid partitions or find the minimum-cost partition.
Input File Format text.

The input file should contain:

     
>#1	   <number_of_cities> <budget_limit><br>
>#2	   Column headers (city labels)<br>
>#3...	    Adjacency matrix: "-" = no connection, numbers= cost<br>


Example:
```
14 9    
A B C D E F G H I J K L M N  
- 3 2 2 8 1 1 6 3 1 1 4 3 7
3 - 8 5 5 1 4 2 8 8 3 4 2 3
2 8 - 7 1 1 3 1 2 8 9 1 6 3
2 5 7 - 3 7 4 3 1 1 2 4 1 3
. . . . . . . . . . . . . .
. . . . . . . . . . . . . . 
. . . . . . . . . . . . . . 
```
## Usage
>`python the-other-thanos-Administration.py <input_file_name>.txt`


## Output<br>
- Default: Lists all valid partitions, with each partition showing paired cities concatenated<br>
- With `-o` flag: Shows only the lowest possible cost
- With `-op` flag: Shows the lowest cost partition(s) along with the cost

# Functions
>`read_data(filename)`

**Purpose & Process**: Parses the input file and extracts the cost matrix. Based on the cost matrix it already calculates cost for each pair and only adds pairs that would not cross the budget limit, so it already includes a first pruning step. It also assumes a minimum cost of 1 for a pairing and adds that into the calculation. So pairing that costs 'x' only gets considered and added if x + number of pairs left < budget. This allows us to eliminate pairs that would almost deplete the completebudget and would certainly exceed the budget when other pairs are added.

**Parameters**: filename specified in command line

**Returns**:<br>
`(municipality_cost, city_list, budget)`<br>
municipality_cost (dict): Keys are (city1, city2) tuples, values are costs. <br>
city_list (list): List of city labels in order.<br>
budget (int): Maximum allowed total cost.<br>

>`find_pairings(unpaired_cities, municipality_cost, budget, current_pairs=None, current_cost=0)`

**Purpose & Process**: Recursively finds all valid city pairings within budget. This also includes some pruning as the minimum cost of a pair is found based on the dictionary. This is used as a multiplier to the pairings still left to be done. It's not specific to each city so it could be improved and calculated for each city but its very simple and already a good way to prune out quite a few possibilities. The function starts with a complete city list as unpaired cities and stops when this list gets empty.

**Parameters**:<br>
unpaired_cities:	List of remaining cities to pair. Starts with full city list<br>
municipality_cost:	Cost dictionary (from read_data) <br>
budget:	Maximum allowed total cost <br>
current_pairs:	Pairs already formed in this recursion branch (default: []) In the first run this gets initialized as an empty list <br>
current_cost:	Sum of costs of already-formed pairs (default: 0) <br>

**Returns**:<br>
`(municipality_list)`
List of valid pairings (municipalities), where each municipality is a list of (city1, city2) tuples.


>`find_minimum(possible_municipalities, municipality_cost, budget)`

**Purpose & Process**: Finds the lowest-cost partition(s) from all valid partitions. Pretty straightforward.

**Parameters**:<br>
possible_municipalities:	All valid municipalities (from find_pairings)<br>
municipality_cost:	Cost dictionary (from read_data)<br>
budget:	Maximum allowed total cost, used to initiate minimum cost variable

**Returns**:<br>
`(lowest_cost, cheapest_municipalities)`<br>
lowest_cost (int): Minimum total cost among all partitions<br>
cheapest_municipalities (list): Partition(s) achieving the minimum cost<br>
