## Parsing and Graph Construction

The program begins by reading the input file. The first line contains two values: the number of cities and the maximum allowed total cost. These values are parsed and converted into integers. The second line provides the list of city names.

Next, all possible city pairs (edges) and their associated costs are extracted from the cost matrix. While doing so, the minimum edge cost is tracked. This value is later used for pruning during the search.

After collecting all edges, an initial lower bound for the remaining cost is computed. Since each valid solution consists of `n/2` pairs, selecting one pair leaves `(n/2 - 1)` pairs to be formed. The minimum possible cost for these remaining pairs is estimated as:
min_remaining_cost = (number_of_remaining_pairs) * (minimum_edge_cost)

Using this bound, edges that can never be part of a valid solution (i.e., those that would exceed the total cost limit even under optimal conditions) are filtered out.

The remaining edges are then used to construct an adjacency list (graph representation), where each city maps to a list of possible partner cities along with the corresponding costs. Since the pairing relationship is symmetric, each edge is added in both directions. This ensures that during the recursive search, every city can correctly access all of its potential partners regardless of the traversal order.

---

## Recursive Pair Generation (Backtracking with Pruning)

The pairing process is implemented using a recursive backtracking function. It takes the following parameters:

- `unpaired`: the list of cities that have not yet been assigned to a pair  
- `graph`: the adjacency list containing valid city pairings  
- `budget`: the maximum allowed total cost  
- `current_pairs`: the list of pairs constructed so far  
- `current_cost`: the accumulated cost of the current partial solution  
- `optimiz`: switch activated with -o flag from terminal
- `best_cost`: alternative for budget during optimization 


### Base Case  
If no cities remain unpaired, a complete valid pairing has been found, and the current solution is returned.

### Recursive Step  
At each step, the algorithm selects the first city from the `unpaired` list. This fixed ordering helps avoid generating duplicate pairings.

For this city, all valid partner cities from the graph are considered. For each candidate partner:

1. It is checked whether the partner is still unpaired.  
2. The new total cost is calculated by adding the cost of this pair.  
3. A pruning condition is applied:  
   - The algorithm estimates the minimum possible cost of completing the remaining pairs.
   - If the current cost plus this lower bound exceeds the budget, the branch is discarded early. In optimize mode this calculated value is compared to the best cost found so far.

If the branch is still feasible:
- The two selected cities are removed from the `unpaired` list.
- The pair is added to `current_pairs`.
- A recursive call is made with the updated state.

The recursion continues until all valid pairings have been explored. As the recursion unwinds, partial solutions are combined into a complete list of valid pairings.
