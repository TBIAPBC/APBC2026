from turtle import distance

from game_utils import Direction as D
from game_utils import TileStatus
from game_utils import Map
from player_base import Player
import numpy as np
from shortestpaths import AllShortestPaths


class BasicBot(Player):

        def __init__(self,*,random=False):
                self.random=random

        def reset(self, player_id, max_players, width, height):
                self.player_name = "Team_1_GoldDigger_left"
                self.ourMap = Map(width, height)
                self.mine_memory = {}
                self.last_junction = None
                self.repositioning_target = None

                self.side = "left"
                self.home_center = (width // 4, height // 3)

        def round_begin(self, r):
                 #map memory
                #store status of fields that you see from the current position
                status = self.status

                #delete expired mines from map and mine memory
                for pos, expiry_round in list(self.mine_memory.items()):
                        if r >= expiry_round:
                                del self.mine_memory[pos]
                                if self.ourMap[pos].status == TileStatus.Mine:
                                        self.ourMap[pos].status = TileStatus.Empty

                for dx in range(-status.params.visibility, status.params.visibility +1):
                        for dy in range(-status.params.visibility, status.params.visibility +1):
                                x = status.x + dx 
                                y = status.y + dy

                                #map boundary
                                if not self.is_inside_map((x, y)):
                                        continue

                                tile_status = status.map[x,y].status

                                if  tile_status != TileStatus.Unknown:
                                        self.ourMap[x,y].status = tile_status

                                        if tile_status == TileStatus.Mine:
                                                if (x,y) not in self.mine_memory:
                                                        self.mine_memory[(x,y)] = r + status.params.mineExpiryTime
                                        elif tile_status == TileStatus.Empty:
                                                self.mine_memory.pop((x,y), None)

        def is_inside_map(self, position):
                x, y = position
                if x < 0 or y < 0:
                                return False
                elif x >= self.ourMap.width or y >= self.ourMap.height:
                                return False
                else:
                        return True

        def _as_direction(self,curpos,nextpos):
                for d in D:
                        diff = d.as_xy()
                        if (curpos[0] + diff[0], curpos[1] + diff[1]) ==  nextpos:
                                return d
                return None

        def _as_directions(self,curpos,path):
                directions = [self._as_direction(x, y) for x, y in zip([curpos] + path, path)]
                return [d for d in directions if d is not None]
        
        def move(self, status):
                ourMap = self.ourMap

                curpos = (status.x,status.y)

                assert len(status.goldPots) > 0
                goldLocation = next(iter(status.goldPots))

                # remember last junction
                neighbours = self.ourMap.nonWallNeighbours(curpos)
                if len(neighbours) >= 3:
                        self.last_junction = curpos
                safe_target = self.get_safe_home_center(curpos)
                
                if not self.is_our_side(goldLocation):
                        safe_target = self.get_safe_home_center(curpos)
                        if safe_target is None:
                                return []
                        else:
                                paths_to_middle = AllShortestPaths(safe_target, self.ourMap)
                                bestpath = paths_to_middle.shortestPathFrom(curpos)
                                if bestpath and len(bestpath) > 0:
                                        bestpath = bestpath[1:]
                                        bestpath.append(safe_target)
                                        numMoves = 1
                                        bestpath = self.check_path(status, bestpath, numMoves)
                                        moves = self._as_directions(curpos, bestpath[:numMoves])
                                        return moves if moves is not None else []

                paths_to_gold = AllShortestPaths(goldLocation, ourMap)
                bestpath = paths_to_gold.shortestPathFrom(curpos)

                # try to find an alternative route avoiding current enemy positions
                enemy_positions = set((o.x, o.y) for o in status.others if o is not None)
                # if the shortest path would step onto an enemy, attempt an alternative
                if any(p in enemy_positions for p in bestpath):
                        alt = paths_to_gold.pathWithAvoidance(curpos, avoid_set=enemy_positions, max_extra=3)
                        if alt and len(alt) <= len(bestpath) + 3:
                                bestpath = alt

                bestpath = bestpath[1:]
                bestpath.append(goldLocation)
                distance = max(0, len(bestpath))
                path_known = all(self.ourMap[pos].status != TileStatus.Unknown for pos in bestpath[1:])
                unknown_count = sum(1 for pos in bestpath if self.ourMap[pos].status == TileStatus.Unknown)

                gold_value = next(iter(status.goldPots.values()))
                low_gold_mode = status.gold < 20
                if low_gold_mode:
                        if distance <= 2:
                                numMoves = min(2, distance)
                        elif path_known and distance <= 4 and gold_value > 15:
                                minimum_dist_move = min(4, distance)
                                if minimum_dist_move * (minimum_dist_move + 1) // 2 <= gold_value:
                                        numMoves = minimum_dist_move
                                else: 
                                        minimum_dist_move = min(3, distance)
                                        if minimum_dist_move * (minimum_dist_move + 1) // 2 <= gold_value:
                                                numMoves = minimum_dist_move

                                        else:
                                                minimum_dist_move = min(2, distance)
                                                if minimum_dist_move * (minimum_dist_move + 1) // 2 <= gold_value:
                                                        numMoves = minimum_dist_move
                                                
                        else:
                                numMoves = 1
                else:
                        numMoves = self.choose_num_moves(status, distance, gold_value, path_known, unknown_count)

                
                if not path_known:
                        if distance > 4:
                                numMoves = min(numMoves, 3)
                        elif distance > 2:
                                numMoves = min(numMoves, 2)

                # if no profitable sprint is found, try to reposition instead of waiting in place
                if numMoves == 0:
                        paths_to_middle = AllShortestPaths(safe_target, self.ourMap)
                        bestpath = paths_to_middle.shortestPathFrom(curpos)
                        if not bestpath:
                                return []
                        bestpath = bestpath[1:]
                        bestpath.append(safe_target)
                        numMoves = 1
        
                bestpath = self.check_path(status, bestpath, numMoves)
                moves = self._as_directions(curpos, bestpath[:numMoves])
                if moves is None:
                        return []
                return moves
        
        def check_path(self, status, path, numMoves):
                i = 0
                for tile in path:
                        if self.check_for_obstacles(status, tile[0], tile[1]):
                                print("collision detected", tile)
                                path = path[:i]
                                break 
                        if self.is_enemy_on_tile(status, tile):
                                print("Enemy detected", tile)
                                path = path[:i]
                                break
                        i+=1
                return path

        def check_for_obstacles(self, status, x, y):
                '''
                checks a given tile for obstacles (walls & mines)
                Input: current status and x, y coordinates of tile to check
                Output: True -> obstacle on tile, False -> tile is clear, None if we cannot see the tile
                '''
                tileStatus = self.ourMap[x, y].status
                # old version: if tile is no wall, we go
                if tileStatus == TileStatus.Wall:
                        return True
                elif tileStatus == TileStatus.Unknown:
                        return None
                return False
                
                # old version: check specifically for walls and mines
                """ if  tileStatus == TileStatus.Wall or tileStatus == TileStatus.Mine:
                        print("Found an obstacle")
                        return True
                elif tileStatus == TileStatus.Unknown: return None
                return False"""

        def is_enemy_on_tile(self, status, pos):
                for other in status.others:
                        if other is not None and (other.x, other.y) == pos:
                                return True
                return False
        
        def choose_num_moves(self, status, distance, gold_value, path_known=False, unknown_count=0):
                best_num_moves = 0
                best_score = 0
                max_affordable = 0
                cost = 0

                while cost < status.gold:
                        max_affordable += 1
                        cost = max_affordable * (max_affordable + 1) // 2
                
                max_affordable -= 1
                max_possible = min(distance, max_affordable)

                if path_known and distance > 0 and distance <= 3:
                        # If the path is fully known and very short, sprint with as much as we can afford.
                        for n in range(max_possible, 0, -1):
                                cost = n * (n + 1) // 2
                                if cost > gold_value * 0.5:
                                        continue

                                expected_gain = gold_value - cost
                                rounds_needed = distance / n
                                if rounds_needed > status.goldPotRemainingRounds or expected_gain <= 0:
                                        continue
                                return n

                for n in range(1, max_possible + 1):
                        cost = n * (n + 1) // 2
                        expected_gain = gold_value - cost

                        # only move if we can afford it and the pot is still reachable in time
                        rounds_needed = distance / n

                        if rounds_needed > status.goldPotRemainingRounds or expected_gain <= 0:
                                continue

                        # prefer high profit, but also prefer reaching the pot sooner
                        # if the path is not fully known, be more conservative in how much we sprint, as we might run into unexpected obstacles
                        if not path_known and unknown_count >= 2 and n > 1:
                                continue
                        if path_known:
                                score = expected_gain - rounds_needed * (4 + 2)
                        else:
                                score = expected_gain - rounds_needed * 4

                        if score > best_score:
                                best_score = score
                                best_num_moves = n

                return best_num_moves

        def is_our_side(self, pos):
                x, y = pos

                if self.side == "left":
                        return x <= self.ourMap.width * 0.6
                else:
                        return x >= self.ourMap.width * 0.4

        def get_safe_home_center(self, curpos):
                x, y = self.home_center
                for dy in range(0, self.ourMap.height // 2, 2):
                        for oy in (dy, -dy):
                                ny = y + oy
                                if 0 <= ny < self.ourMap.height and self.ourMap[x, ny].status != TileStatus.Wall:
                                        return (x, ny)
                return curpos

players = [ BasicBot()]
