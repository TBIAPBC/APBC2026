#!/usr/bin/env python3
import copy
import math
import random
import argparse
import sys
import os
from contextlib import redirect_stdout 

import game_utils
import simulator
import player_base
import shortestpaths
from game_utils import nameFromPlayerId
from game_utils import Direction as D, MoveStatus
from game_utils import Tile, TileStatus, TileObject
from game_utils import Map, Status
from illustrator import Illustrator
from simulator import Simulator
from player_base import Player

parser = argparse.ArgumentParser(description="Robot Race Simulator 7000")
parser.add_argument('--viz', help="filename for the visualization of the race", type=str)
parser.add_argument('--number', help="number of rounds", type=int, default=1000)
parser.add_argument('--density', help="map density", type=float, default=0.4)
parser.add_argument('--framerate', help="specify framerate of the visualization", type=int, default=8)
parser.add_argument('--map', help="specify map file", type=str,default=None)
parser.add_argument('--mine_mode', help="specify what mines do. Options are wall, scramble and damage", type=str, default="wall")
parser.add_argument('--allow_jumps', help="allow players to jump over walls by running into the same direction twice", action=argparse.BooleanOptionalAction)
parser.add_argument('--games', help="number of games to simulate", type=int, default=1)

args = parser.parse_args()

# Add your robot player here
robot_module_names = {
                      "StalkerHunter_Stalker": "stalkerhunter_stats-RobotRace",
                      "round_2_bot":"round_2_bot-RobotRace",
                      "Beatme_SillyScout": "beatme-RobotRace",
                      "Test": "test-RobotRace",
                      }


# Ensure that the robot is the correct directory. It will search for a subdirectory from the local script directory
# In this case the subdirectory from the local script directory is "Robots"
script_dir = os.path.dirname(os.path.realpath(__file__))
robots_dir = os.path.join(script_dir, 'Robots')
sys.path.insert(0, robots_dir)

robotmodules = { m:__import__(m) for m in robot_module_names.values() }

if args.map is not None:
   base_map = Map.read(args.map)
else:
   base_map = Map.makeRandom(30, 30, args.density)

win_stats = {name: 0 for name in robot_module_names.keys()}
win_stats["Draw/None"] = 0
move_stats = {name: 0 for name in robot_module_names.keys()}

health_stats = {name: 0 for name in robot_module_names.keys()}
distance_stats = {name: 0 for name in robot_module_names.keys()}
gold_stats = {name: 0 for name in robot_module_names.keys()}

# NEW: rank tracking (sum of ranks across games, for averaging later)
rank_stats = {name: 0 for name in robot_module_names.keys()}

# NEW: best victory tracking — stores (gold_amount, game_num) per player
best_victory = {name: None for name in robot_module_names.keys()}  # None = no win yet

is_batch_run = args.games > 1

if is_batch_run:
    print(f"Starting {args.games} games silently... Please wait.")

def attach_tracker(player_obj, method_name):
    original_brain = getattr(player_obj, method_name)
    
    def intercepted(*args, **kwargs):
        status = None
        for arg in args:
            if hasattr(arg, 'x') and hasattr(arg, 'y'):
                status = arg
                break
        if not status and 'status' in kwargs:
            status = kwargs['status']
            
        if status:
            if player_obj.last_pos is not None:
                dx = status.x - player_obj.last_pos[0]
                dy = status.y - player_obj.last_pos[1]
                distance = math.sqrt(dx**2 + dy**2)
                player_obj.total_distance += distance
            
            player_obj.last_pos = (status.x, status.y)

        raw_moves = original_brain(*args, **kwargs)
        moves_list = [] if raw_moves is None else list(raw_moves)
            
        if moves_list:
            player_obj.total_moves_made += len(moves_list)
            
        return moves_list
        
    setattr(player_obj, method_name, intercepted)

for game_num in range(args.games):

    # NEW: decide viz filename for this game:
    # - In single-game mode, use args.viz as-is (original behaviour).
    # - In batch mode we don't know the winner yet, so we write to a temp file and
    #   rename it afterwards if it turns out to be a best-victory game.
    if not is_batch_run:
        current_viz = args.viz
    else:
        # Use a temp file so we can rename it if needed; None means no viz at all.
        # We only bother generating a viz file when args.viz is set.
        current_viz = f"__temp_viz_game_{game_num}.gif" if args.viz else None

    sim = Simulator(map=base_map, vizfile=current_viz, framerate=args.framerate)
    
    # This doesn't silence all output, but it will silence the print statements from the Simulator when running in batch mode
    if is_batch_run:
        sim.printInitial = False
        sim.printRoundBegin = False
        sim.printEvents = False
        sim.printMoves = False

    team_mapping = []

    for name, module_name in robot_module_names.items():
        for p in robotmodules[module_name].players:
            fresh_player = copy.deepcopy(p) 
            fresh_player.player_modname = name
            
            # Initialization
            fresh_player.total_moves_made = 0
            fresh_player.total_distance = 0.0  
            fresh_player.gold_collected = 0
            fresh_player.last_pos = None      
            
            if hasattr(fresh_player, 'move'):
                attach_tracker(fresh_player, 'move')

            sim.add_player(fresh_player)
            team_mapping.append(fresh_player)

    if not is_batch_run:
        print(f"Running Game {game_num + 1}/{args.games}...", end="\r")
    
    if is_batch_run:
        # redirect_stdout silences all print outputs that are still remaining from other modules
        with open(os.devnull, 'w') as f, redirect_stdout(f):
            result = sim.play(rounds=args.number, jumps_allowed=args.allow_jumps, mine_mode=args.mine_mode.lower())
    else:
        result = sim.play(rounds=args.number, jumps_allowed=args.allow_jumps, mine_mode=args.mine_mode.lower())

    # ---- Collect gold scores for this game so we can rank players ----
    game_gold = {}   # team_name -> gold earned this game

    winner_name = None
    max_gold = -1
    
    for i, player_obj in enumerate(team_mapping):
        team_name = player_obj.player_modname 
        player_gold = 0
        player_health = 0
        
        if len(sim._status) > i:
            status = sim._status[i]
            player_gold = status.gold
            player_health = status.health  

        if player_gold > max_gold:
            max_gold = player_gold
            winner_name = team_name
        elif player_gold == max_gold:
            winner_name = "Draw/None"
            
        health_stats[team_name] += player_health
        distance_stats[team_name] += player_obj.total_distance
        gold_stats[team_name] += player_gold
        game_gold[team_name] = player_gold

    if winner_name:
        win_stats[winner_name] += 1

    # ---- NEW: compute per-player rank for this game ----
    # Sort by gold descending; ties get the same (best) rank.
    sorted_teams = sorted(
        [n for n in robot_module_names.keys()],
        key=lambda n: game_gold.get(n, 0),
        reverse=True
    )

    assigned_rank = {}
    prev_gold = None
    prev_rank = None
    for rank_idx, tname in enumerate(sorted_teams, start=1):
        g = game_gold.get(tname, 0)
        if g == prev_gold:
            assigned_rank[tname] = prev_rank   # tied → same rank
        else:
            assigned_rank[tname] = rank_idx
            prev_rank = rank_idx
            prev_gold = g

    for tname, rank in assigned_rank.items():
        rank_stats[tname] += rank

    for player_obj in team_mapping:
        team_name = player_obj.player_modname
        move_stats[team_name] += player_obj.total_moves_made

    # ---- NEW: best-victory visualization bookkeeping ----
    if args.viz and is_batch_run:
        # Determine the actual winner(s) of this game (could be a tie)
        winners_this_game = [
            t for t in robot_module_names.keys()
            if game_gold.get(t, 0) == max_gold and winner_name != "Draw/None"
        ]

        claimed = False   # did any player "claim" this viz file?
        for w in winners_this_game:
            w_gold = game_gold.get(w, 0)
            if best_victory[w] is None or w_gold > best_victory[w][0]:
                # This is the best win so far for player w — remember which temp file holds it
                best_victory[w] = (w_gold, current_viz)
                claimed = True

        if not claimed and current_viz and os.path.exists(current_viz):
            os.remove(current_viz)   # nobody needs this viz → discard it

# ---- NEW: rename/copy best-victory temp files to final named files ----
if args.viz and is_batch_run:
    base, ext = os.path.splitext(args.viz)
    if not ext:
        ext = ".gif"

    # Track which temp files have been "consumed" (renamed) so we don't double-use
    used_temp_files = set()

    for team_name, victory_info in best_victory.items():
        if victory_info is None:
            continue   # player never won

        gold_amount, temp_path = victory_info
        if not temp_path or not os.path.exists(temp_path):
            continue

        safe_name = team_name.replace(" ", "_").replace("/", "-")
        final_path = f"{base}_best_victory_{safe_name}{ext}"

        if temp_path in used_temp_files:
            # Two players share the same best-victory file (tie game) — copy instead of rename
            import shutil
            shutil.copy2(temp_path, final_path)
        else:
            os.rename(temp_path, final_path)
            used_temp_files.add(temp_path)

        print(f"  Saved best victory viz for [{team_name}] "
              f"(gold: {gold_amount}) → {final_path}")

    # Clean up any remaining unused temp files
    for team_name, victory_info in best_victory.items():
        if victory_info is None:
            continue
        _, temp_path = victory_info
        if temp_path and os.path.exists(temp_path) and temp_path not in used_temp_files:
            os.remove(temp_path)

    # Also remove any stray temp files from games where nobody won (ties throughout)
    for game_num in range(args.games):
        stray = f"__temp_viz_game_{game_num}.gif"
        if os.path.exists(stray):
            os.remove(stray)

print("\n--- STATISTICAL ANALYSIS ---\n")
num_bots = len(robot_module_names)
for team, wins in win_stats.items():
    win_rate = (wins / args.games) * 100
    
    if team == "Draw/None":
        print(f"Draws/Ties: {wins} games ({win_rate:.1f}%)\n")
    else:
        avg_moves = move_stats[team] / args.games
        avg_health = health_stats[team] / args.games
        avg_distance = distance_stats[team] / args.games
        avg_gold = gold_stats[team] / args.games
        avg_rank = rank_stats[team] / args.games   # NEW

        # NEW: best-victory footnote
        bv = best_victory.get(team)
        bv_str = f" | Best Victory Gold: {bv[0]}" if bv else " | Best Victory Gold: N/A"

        print(f"{team}: {wins} wins ({win_rate:.1f}%) | "
              f"Avg Rank: {avg_rank:.2f} | "
              f"Avg Gold: {avg_gold:.1f} | "
              f"Avg Distance: {avg_distance:.1f} | "
              f"Avg Moves: {avg_moves:.1f} | "
              f"Avg Health: {avg_health:.1f}"
              f"{bv_str}\n")