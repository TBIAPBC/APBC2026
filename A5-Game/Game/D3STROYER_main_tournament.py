# compete against the provided test players by running runRobotRace.py
# adapt the file runRobotRace.py: register your module in robot_module_names
# python3 runRobotRace.py --number 100 --viz viz.gif
# file has to be in Game folder.
# extract frames:
# ffmpeg -i viz.gif -vf "select=eq(n\,0)" -q:v 3 firstframe.png

import math
import copy
from collections import deque
from game_utils import Direction as D
from game_utils import TileStatus
from game_utils import Map
from player_base import Player
from shortestpaths import AllShortestPaths

# =================================
# Tuning constants
# =================================

#  escape exit if we crash
STUCK_EXIT = 3
MEMORY_LEN = 8

# What map are we playing on ?
MAZE_DENSITY = 0.28     #above, we say it is maze map
MAP_SAMPLE_ROUNDS = 10  #rounds before we decide on strategy

# Moves per map type
# Open map
#git makes me sad
OPEN_BIG = 6    # pot > 50
OPEN_MID = 4    # pot > 20 
OPEN_SMALL = 2  # small pot 
# Maze map
MAZE_BIG = 5
MAZE_MID = 3
MAZE_SMALL = 2

# score weights
DIST_PEN = 2       # gold lost per step of distance
ENEMY_CLOSER = 25 

# waiting strategy for low gold situations
WAIT = 8 # rounds of saving beats moving on


class neo(Player):

    def reset(self, player_id, max_players, width, height):
        self.player_name = "D3STROYER_A"
        self.ourMap = Map(width, height)
        #print(len(self.ourMap[0]))

        # position hist to detect stuck situations
        #self._pos_history: list[tuple] = []
        self._last_pos = None
        self._stuck_streak = 0
        self._last_action = None
        self._prev_action = None

        # escape mode
        self._escape_mode = False
        self._escape_path: list[tuple] = []
        self._escape_cooldown = 0
        # map type detection
        self._wall_count = 0
        self._known_count = 0
        self._map_type = "unknown"  # "maze" | "open" | "unknown"
        self._round_num = 0
        self._even_known = 0
        self._even_walls = 0
        self._odd_known = 0
        self._odd_walls = 0
        # repositioning (map fully explored & nothing to do)
        self._center = (width // 2, height // 2)
        self._cavesgoal = (8, 35)

        # Jumping
        self._jumps_ok = False #updated with first move call

    def round_begin(self, r):
        self._round_num = r
        #pass
    
    # ---- direction helpers ----
    def _as_direction(self,curpos,nextpos):
            for d in D:
                diff = d.as_xy()
                if (curpos[0] + diff[0], curpos[1] + diff[1]) ==  nextpos:
                    #print(d)
                    return d  
            return None

    def _as_directions(self,curpos,path):
            return [self._as_direction(x,y) for x,y in zip([curpos]+path,path)]
    
    # ---- Map helpers ---
    def _update_map(self, status):
        for x in range(self.ourMap.width):
            for y in range(self.ourMap.height):

                tile = status.map[x, y]

                if tile.status == TileStatus.Unknown:
                    continue

                old = self.ourMap[x, y].status   # IMPORTANT: capture BEFORE update

                self.ourMap[x, y].status = tile.status

                # only count NEW discoveries
                if old == TileStatus.Unknown:

                    self._known_count += 1

                    if tile.status == TileStatus.Wall:
                        self._wall_count += 1

                    y_parity = y & 1

                    if y_parity == 0:
                        self._even_known += 1
                        if tile.status == TileStatus.Wall:
                            self._even_walls += 1
                    else:
                        self._odd_known += 1
                        if tile.status == TileStatus.Wall:
                            self._odd_walls += 1
    
    def _is_alternating_maze(self):
        if self._even_known < 35 or self._odd_known < 35:
            #print('havent seen enough')
            return False

        even = self._even_walls / self._even_known
        odd = self._odd_walls / self._odd_known
        #print(f"even={even:.2f} ({self._even_walls}/{self._even_known}) "f"odd={odd:.2f} ({self._odd_walls}/{self._odd_known})")
        return abs(even - odd) > 0.4 and max(even, odd) > 21/30
    
    def _update_map_type(self):
        
        if self._map_type != "unknown":
            #print('i didnt recognize unknown')
            return
        w = self.ourMap.width
        if w > 30:
            self._map_type = "caves"
        if self._is_alternating_maze():
            self._map_type = "maze"
            return
        
        if self._round_num >= MAP_SAMPLE_ROUNDS:
            self._map_type = "open"
        

    def _map_bounds(self, pos):
        x, y = pos
        
        if x < 0 or x >= self.ourMap.width:
            return False

        if y < 0 or y >= self.ourMap.height:
            return False

        return True
    
    
    def _adj_cells(self, pos, use_jumps=False):
        x,y = pos
        for d in D:
            dx, dy = d.as_xy()
            nxt = (x + dx, y + dy)
            if not self._map_bounds(nxt):
                continue
            tile_status = self.ourMap[nxt].status
            if tile_status != TileStatus.Wall:
                yield nxt
            elif use_jumps:
                jump = (x+2 * dx, y + 2 * dy)
                if self._map_bounds(jump) and self.ourMap[jump].status == TileStatus.Empty:
                    yield jump

    # ---- frontier exploration ----

    def _is_frontier(self, pos):

        if self.ourMap[pos].status != TileStatus.Empty:
            return False

        for cell in self._adj_cells(pos):

            if self.ourMap[cell].status == TileStatus.Unknown:
                return True

        return False
    
    def _shortest_path_to_target(self, start, target_fn, use_jumps = False):
        queue = deque([start])
        visited = {start}
        prev = {}

        while queue:
            cur = queue.popleft()

            if target_fn(cur):
                path = [cur]

                while cur in prev:
                    cur = prev[cur]
                    path.append(cur)

                path.reverse()
                return path

            for nxt in self._adj_cells(cur, use_jumps=use_jumps):
                if nxt in visited:
                    continue

                if self.ourMap[nxt].status not in (
                    TileStatus.Empty,
                    TileStatus.Unknown
                ):
                    continue

                visited.add(nxt)
                prev[nxt] = cur
                queue.append(nxt)

        return []
    
    def _shortest_path_to_frontier(self, start):
        return self._shortest_path_to_target(start, self._is_frontier, use_jumps=self._jumps_ok)
    
    def _shortest_path_to_pos(self, start, target):
        return self._shortest_path_to_target(start, lambda p: p == target, use_jumps=self._jumps_ok)
    
    # Escape logic if stuck
    def _update_history(self, pos):
        self._pos_history.append(pos)
        if len(self._pos_history) > MEMORY_LEN:
            self._pos_history.pop(0)

    def _is_stuck(self, curpos):
        if self._last_pos is None:
            self._last_pos = curpos
            return False
        
        if self._last_action == []:
            self._last_pos = curpos
            self._stuck_streak = 0
            return False

        same_position = (curpos == self._last_pos)
        same_action = (self._last_action == self._prev_action)

        if same_position and same_action:
            self._stuck_streak += 1
        else:
            self._stuck_streak = 0

        self._last_pos = curpos

        return self._stuck_streak >= 2
    
    def _local_escape(self, curpos, status):
        candidates = self._adj_cells(curpos, use_jumps=self._jumps_ok)

        best = None

        for nxt in candidates:
            if self.ourMap[nxt].status != TileStatus.Wall:
                for other_status in status.others:
                    if other_status is None:
                        continue

                    x, y = (other_status.x, other_status.y)
                    self.ourMap[x, y].status = TileStatus.Wall
                if self.ourMap[nxt].status == TileStatus.Empty:
                    return [nxt]
                best = best or nxt

        return [best] if best else []
    
    def _escape_direction(self, curpos):
        blocked = set(self._pos_history[-MEMORY_LEN:])

        queue = deque([curpos])
        visited = {curpos}
        prev = {}

        while queue:
            cur = queue.popleft()

            if cur != curpos and self._is_frontier(cur):
                path = []
                node = cur

                while node in prev:
                    path.append(node)
                    node = prev[node]

                path.reverse()
                return path

            for nxt in self._adj_cells(cur, use_jumps=self._jumps_ok):

                if nxt in visited:
                    continue

                if self.ourMap[nxt].status == TileStatus.Wall:
                    continue

                # soft blocking (IMPORTANT: not hard block)
                if nxt in blocked:
                    continue

                visited.add(nxt)
                prev[nxt] = cur
                queue.append(nxt)

        return []

    # ---- Cost helper ----
    def _affordable_moves(self, gold):
        """
        How many moves can we afford?
        cost(k) = 1+2+...+k = k*(k+1)/2  ≤ gold
        Solve for largest k where k*(k+1)/2 ≤ gold.
        """
        k = 0
        while (k+1) * (k+2) // 2 <= gold:
            k += 1
        return k 
    
    @staticmethod
    def _movement_cost(distance):
        return distance * (distance + 1) // 2

    # not used at the moment
    def _found_gold(self, status, gx, gy):
        # returns True if gold is in visible map
        tile = status.map[gx, gy]
        return tile.status != TileStatus.Unknown 

    #---- waiting strategy  ----
    def _should_wait(self, status, distance, pot_value):
        """
            option A: go now 
            option B: wait k rounds, then go
        """
        if self._map_type == "maze":
            return False # in maze moving is almost always better
        
        max_moves = self._affordable_moves(status.gold)
        move_cost = neo._movement_cost(min(max_moves, distance))
        if move_cost > pot_value:
            return True
        #return deficit > WAIT
    
    # ---- Gold target -----
    def _best_gold_target(self, status, curpos):
        best_score = float("-inf")
        best_gold = None
        best_path = None

        for gLoc, gold_value in status.goldPots.items():
            tempMap = copy.deepcopy(self.ourMap)
            paths = AllShortestPaths(gLoc, tempMap)
            
            pot_value = status.goldPots[gLoc]
            my_path = paths.shortestPathFrom(curpos)

            if not my_path:
                continue

            my_path = my_path[1:]
            my_path.append(gLoc)

            my_distance = len(my_path)

            enemy_wins = False

            for other_status in status.others:
                if other_status is None:
                    continue

                enemy_pos = (other_status.x, other_status.y)

                enemy_path = paths.shortestPathFrom(enemy_pos)

                if not enemy_path:
                    continue

                enemy_distance = len(enemy_path)

                enemy_can_afford = (
                self._movement_cost(enemy_distance) <= other_status.gold
                and pot_value >= self._movement_cost(enemy_distance) + 30
            )

                if enemy_can_afford and enemy_distance < my_distance:
                    enemy_wins = True
                    #print(f'found enemy at {enemy_pos}')
                    break

            if enemy_wins:
                continue

            score = gold_value - self._movement_cost(my_distance)

            if score > best_score:
                best_score = score
                best_gold = gLoc
                best_path = my_path

        return best_gold, best_path

    def _num_moves_to_make(self, status, distance, pot_value):
        max_affordable = self._affordable_moves(status.gold)

        if self._map_type == "open":
            if pot_value > 50:
                base = OPEN_BIG
            elif pot_value > 20:
                base = OPEN_MID
            else:
                base = OPEN_SMALL
        else:
            # maze or unknown
            if pot_value > 50:
                base = MAZE_BIG
            elif pot_value > 20:
                base = MAZE_MID
            else:
                base = MAZE_SMALL

        n = min(base, distance, max_affordable)


        while n > 0 and self._movement_cost(n) >= pot_value:
            n -= 1


        if self._map_type == "open":
            if (self._movement_cost(distance) < max_affordable and
                self._movement_cost(distance) <= pot_value - 10):
                n = distance

        elif self._map_type == "maze":
            n = 3
        elif self._map_type =="caves":
            if (self._movement_cost(distance) < max_affordable and
                self._movement_cost(distance) <= pot_value - 10):
                n = distance

        return n
    
    def _reposition_to_center(self, curpos):
        #move to center if nothing to do
        if self._map_type == "caves":
            cx, cy = self._cavesgoal
        else:
            cx, cy = self._center
        if curpos == self._center:
            #print(self._center)
            return []
        
        if self.ourMap[cx, cy].status != TileStatus.Empty:
            # find nearest empty cell to center
            for radius in range(1, max(self.ourMap.width, self.ourMap.height)):
                found = False
                for dx in range(-radius, radius + 1):
                    for dy in range(-radius, radius + 1):
                        if abs(dx) != radius and abs(dy) != radius:
                            continue
                        nx, ny = cx + dx, cy + dy
                        if (self._map_bounds((nx, ny)) and
                                self.ourMap[nx, ny].status == TileStatus.Empty):
                            self._center = (nx, ny)
                            found = True
                            break
                    if found:
                        break
                if found:
                    break
        if self._map_type == "caves":
            path = self._shortest_path_to_pos(curpos, self._cavesgoal)
        else:
            path = self._shortest_path_to_pos(curpos, self._center)
        # already close enough
        if path and len(path) - 1 <= 5:
            return []
        return path
    
    def _register_action(self, action):
        self._prev_action = self._last_action
        self._last_action = action
    
    def move(self, status):
        self._update_map(status)
        self._update_map_type()
        #print(self._map_type)
        try:
            self._jumps_ok = status.params.jumps_ok
        except AttributeError:
            self._jumps_ok = False

        curpos = (status.x,status.y)

        assert len(status.goldPots) > 0

        # escape mode
        if self._is_stuck(curpos):
            #print("ENTER ESCAPE MODE")
            self._escape_mode = True
            self._escape_cooldown = 3
        
        # TO-DO: in low gold situations, we now do one step per round towards gold, change to center, or to no moves at all ?
        if self._escape_mode:

            #print("ESCAPE MODE ACTIVE", curpos)

            # exit condition: no longer stuck
            if not self._is_stuck(curpos):
                self._escape_cooldown -= 1
                if self._escape_cooldown <= 0:
                    #print("EXIT ESCAPE MODE")
                    self._escape_mode = False
                    self._escape_path = []
                    #print("cooldown active:", self._escape_cooldown)

            # generate path ONLY if needed
            if not self._escape_path:
                self._escape_path = self._local_escape(curpos, status)

                if not self._escape_path:
                    self._escape_path = self._escape_direction(curpos)

                if not self._escape_path:
                    self._escape_mode = False
                    return self._fallback_move(status, curpos)

                self._escape_i = 0

            # follow path
            if self._escape_i >= len(self._escape_path):
                #print("escape path finished")
                self._escape_mode = False
                self._escape_path = []
                return self._fallback_move(status, curpos)

            step = self._escape_path[self._escape_i:self._escape_i + 1]
            self._escape_i += 1

            action = self._as_directions(curpos, step)
            self._register_action(action)
            return action

        # find best gold target
        gLoc, bestpath = self._best_gold_target(status, curpos)

        if bestpath is None:
            #print('enemy closer so use fallback moves')
            return self._fallback_move(status, curpos)
        
        distance = len(bestpath)

        pot_value = status.goldPots[gLoc]
        
        if pot_value < self._movement_cost(distance):
            #print('is the pot too far away??')
            return self._fallback_move(status, curpos)

        if self._should_wait(status, distance, pot_value):
            #print('are we waiting?')
            return self._fallback_move(status, curpos)
        
        numMoves = self._num_moves_to_make(status, distance, pot_value)
        
        if distance//2 > status.goldPotRemainingRounds:
            if self._affordable_moves(status.gold) < self._movement_cost(distance):
                #print('is the pot too far away 2??')
                return self._fallback_move(status, curpos)
            else:
                action = self._as_directions(curpos, bestpath[:numMoves])
                self._register_action(action)
                #print('stuck at this weird check')
                return self._as_directions(curpos,bestpath[:numMoves])

        if numMoves == 0:
            #print('are we out of moves?')
            return self._fallback_move(status, curpos)
        #print('reached end of moves')
        action = self._as_directions(curpos, bestpath[:numMoves])
        self._register_action(action)
        return self._as_directions(curpos,bestpath[:numMoves])
    
    def _fallback_move(self, status, curpos):
        gLoc, bestpath = self._best_gold_target(status, curpos)
        #print('in fallback')
        if bestpath!= None:
            distance = len(bestpath)
        else:
            distance = 999
            
        if distance > status.goldPotRemainingRounds:
            frontier_path = self._shortest_path_to_frontier(curpos)
            if len(frontier_path) >= 1:
                if self._map_type != "caves":
                    print(f'neo wants to move to a frontier')
                    steps = min(2, len(frontier_path))
                    action = self._as_directions(curpos, frontier_path[1:steps+1])
                    self._register_action(action)
                    return self._as_directions(curpos, frontier_path[1:steps+1])
                
    
            # fully explored — reposition to center so we're ready for next gold pot
            center_path = self._reposition_to_center(curpos)
            if center_path:
                print('i want to move to the middle')
                action = self._as_directions(curpos, center_path[1:2])
                self._register_action(action)
                return self._as_directions(curpos, center_path[1:2])
        else:
            print(f'neo wants to move to the pot (slowly)')
            if status.gold < 10:
                #print(f'i only have {status.gold} gold so I will wait')
                return []
            else: 
                action = self._as_directions(curpos, bestpath[:1])
                self._register_action(action)
                return self._as_directions(curpos, bestpath[:1])
 
        return []


    def set_mines(self, status):
        """
        The player answers with a list of positions, where mines
        should be set.
        """
        raise NotImplementedError("'setting mines' not implemented in '%s'." % self.__class__)

players = [ neo()]