# compete against the provided test players by running runRobotRace.py
# adapt the file runRobotRace.py: register your module in robot_module_names
# python3 runRobotRace.py --number 100 --viz viz.gif
# file has to be in Game folder.
# extract frames:
# ffmpeg -i viz.gif -vf "select=eq(n\,0)" -q:v 3 firstframe.png

import math
import copy
from game_utils import Direction as D
from game_utils import TileStatus
from game_utils import Map
from player_base import Player
from shortestpaths import AllShortestPaths


class D3STROYER(Player):

    # ------------ Tuning parameters --------------------
    # If expected_profit < MIN_POFIT -> skip pot
    MIN_PROFIT = 20

    # Rounds of margin required beyond the bare minimum travel time
    # E.g. 1.5x the distance in remaining rounds
    ROUNDS_SAFETY_MARGIN = 1.5

    # If enemy is much closer, skip pot
    # 0.85 = skip if enemy needs ≤ 85% of our steps
    OPPONENT_DISTANCE = 0.85

    # Blacklist tiles on each enemy path, to avoid crashes
    BLACKLIST_DEPTH = 2

    # Keep gold reserve
    GOLD_REVERSE = 10   
    
    # ------------------------------------------------

    def reset(self, player_id, max_players, width, height):
        self.player_name = "D3STROYER"
        self.ourMap = Map(width, height)

    def round_begin(self, r):
        pass

    # ------------------------------------------------
    
    # helpers
    def _as_direction(self,curpos,nextpos):
            for d in D:
                    diff = d.as_xy()
                    if (curpos[0] + diff[0], curpos[1] + diff[1]) ==  nextpos:
                            return d
            return None

    def _as_directions(self,curpos,path):
            return [self._as_direction(x,y) for x,y in zip([curpos]+path,path)]
    
    def _update_map(self, status):
        for x in range(self.ourMap.width):
            for y in range(self.ourMap.height):
                if status.map[x,y].status != TileStatus.Unknown:
                    self.ourMap[x,y].status = status.map[x,y].status

    @staticmethod
    def _movement_cost(distance):
        return distance * (distance + 1) // 2
    
    def _affordable_moves(self, gold):
        """
        How many moves can we afford?
        cost(k) = 1+2+...+k = k*(k+1)/2  ≤ gold
        """
        k = 0
        while (k+1) * (k+2) // 2 <= gold - self.GOLD_REVERSE:
            k += 1
        return k
    
    def _enemy_min_distance(self, status, paths):
        """
         Returns shortest path visible enemy has to Gold.
         Return None if no enemies visible.
        """
        min_dist = None
        for other in status.others:
             if other is not None:
                  other_path = paths.shortestPathFrom((other.x, other.y))
                  # start -> length -1 = steps
                  dist = len(other_path)-1
                  if dist >= 0 and (min_dist is None or dist < min_dist):
                       min_dist = dist
        return min_dist
    
    def _pot_is_viable(self, status, distance, pot_value, enemy_min_dist):
        """
        Chase pot or not ? 
        """
        cost = self._movement_cost(distance)
        spendable_gold = status.gold - self.GOLD_REVERSE

        # 1. Can we afford walk at all?
        if cost > spendable_gold:
            return False, "cant_afford"
        
        # 2. If pot worth it?
        profit = pot_value - cost
        if profit < self.MIN_PROFIT:
            return False, "low_profit"
        
        # 3. Enough rounds left?
        rounds_needed = distance * self.ROUNDS_SAFETY_MARGIN
        if rounds_needed > status.goldPotRemainingRounds:
            return False, "too_little_rounds"
         
        #4. Is enemy faste?
        if enemy_min_dist is not None:
            if enemy_min_dist <= distance * self.OPPONENT_DISTANCE:
                return False, "opponent_faster"
        
        return True, "go"
    
    def _choose_num_moves(self, status, distance, pot_value, viable):
        """
        How many moves this turn? 

        strategy:
            - Not viable -> 0 (stand still)
            - Faster AND pot is big enough -> sprint all the way
            - Otherwise -> 2-3 moves 
        """

        if not viable:
             return 0
        
        spendable = status.gold - self.GOLD_REVERSE
        budget_moves = self._affordable_moves(status.gold)

        full_cost = self._movement_cost(distance)

        # sprint if we are faster and pot is profitable
        sprint_profit = pot_value - full_cost
        if full_cost <= spendable and sprint_profit >= self.MIN_PROFIT * 2:
             return min(distance, budget_moves)
        
        # move 2-3 steps depending on budget -> durch expoloration logik ersetzen
        default_moves = 3 if budget_moves >= 3 else budget_moves
        return max(0, default_moves)


    def _found_gold(self, status, gx, gy):
        # returns True if gold is in visible map
        tile = status.map[gx, gy]
        return tile.status != TileStatus.Unknown 

    # Main move logic
    def move(self, status):
        self._update_map(status)

        curpos = (status.x,status.y)

        assert len(status.goldPots) > 0
        # possible edge case: multiple gold pots exist
        #gLoc = next(iter(status.goldPots)) # only one gold pot
        gLoc = max(status.goldPots, key=lambda loc: status.goldPots[loc]) # more than one gold pot
        pot_value = status.goldPots[gLoc]

        # 1. compute path on temporary map 
        # copy map that ours dont get corrupted
        tempMap = copy.deepcopy(self.ourMap)

        ## determine next move d based on shortest path finding
        paths_raw = AllShortestPaths(gLoc,tempMap)

        # opponent min distance
        opponent_min_dist = self._enemy_min_distance(status, paths_raw)

        # 2. blacklisting enemys paths
        for other in status.others:
            if other is not None:
                other_pos = other.x, other.y
                other_path = paths_raw.shortestPathFrom(other_pos)
                # blacklist first n predicted path tiles
                for tile in other_path[1: self.BLACKLIST_DEPTH + 1]:
                    tempMap[tile].status = TileStatus.Wall

        # recompute paths after Map update to avoid other players
        paths = AllShortestPaths(gLoc,tempMap)
        bestpath = paths.shortestPathFrom(curpos)
        
        # 3. extract distance
        # distance = len(path) -1 , and moves slice in path[1:]
        if len(bestpath) < 2:
            return [] # unreachable
        
        move_path = bestpath[1:] # path without start position
        distance = len(move_path) # num of steps to goal

        # 4. viability + numMoves
        viable, reason = self._pot_is_viable(status, distance, pot_value, opponent_min_dist)
        numMoves = self._choose_num_moves(status, distance, pot_value, viable)

        # 5. reposition, if skipping the pot
        if numMoves == 0:
            # move towards center
            cx, cy = self.ourMap.width // 2, self.ourMap.height //2
            center = (cx,cy)
            if curpos != center:
                center_map = copy.deepcopy(self.ourMap)
                center_paths = AllShortestPaths(center, center_map)
                center_path = center_paths.shortestPathFrom(curpos)
                if len(center_path) >= 2:
                    reposition_moves = min(2, self._affordable_moves(status.gold))

                    return self._as_directions(curpos, center_path[1:1 + reposition_moves])
                return[]
            
        return self._as_directions(curpos, move_path[:numMoves])
    

    def set_mines(self, status):
        """
        The player answers with a list of positions, where mines
        should be set.
        """
        raise NotImplementedError("'setting mines' not implemented in '%s'." % self.__class__)

players = [ D3STROYER()]
