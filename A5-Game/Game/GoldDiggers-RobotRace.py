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
                self.player_name = "Team_1_GoldDigger"
                self.ourMap = Map(width, height)
                self.mine_memory = {}

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
                return [self._as_direction(x,y) for x,y in zip([curpos]+path,path)]

        def move(self, status):
                ourMap = self.ourMap

                #print("-" * 80)
                #print("Status for %s" % self.player_name)
                #print(status)

                curpos = (status.x,status.y)

                assert len(status.goldPots) > 0
                gLoc = next(iter(status.goldPots))

                ## move towards gold pot

                numMoves = 2

                paths = AllShortestPaths(gLoc,ourMap)
                bestpath = paths.shortestPathFrom(curpos)

                bestpath = bestpath[1:]
                bestpath.append( gLoc )

                distance=len(bestpath)

                
                #TODO: also check for total remaining rounds in the game
                if numMoves>0 and distance/numMoves > status.goldPotRemainingRounds:
                        numMoves = 0
                        print("BasicBot: Closest Pot too far -> waiting mode")

                return self._as_directions(curpos,bestpath[:numMoves])
        
        def check_for_obstacles(self, status, x, y):
                '''
                checks a given tile for obstacles (walls & mines)
                Input: current status and x, y coordinates of tile to check
                Output: True -> obstacle on tile, False -> tile is clear, None if we cannot see the tile
                '''
                tileStatus = self.ourMap[x, y].status
                if  tileStatus == TileStatus.Wall or tileStatus == TileStatus.Mine:
                        print("Found an obstacle")
                        return True
                elif tileStatus == TileStatus.Unknown: return None
                return False

players = [ BasicBot()]
