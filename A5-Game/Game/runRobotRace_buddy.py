#!/usr/bin/env python3
import argparse
import io
import os
from collections import Counter
from contextlib import redirect_stdout

from game_utils import nameFromPlayerId
from game_utils import Direction as D, MoveStatus
from game_utils import Tile, TileStatus, TileObject
from game_utils import Map, Status
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
parser.add_argument('--games', help="number of games to run", type=int, default=1)

args = parser.parse_args()

robot_module_names = {
        "GoldDiggers_left": "GoldDiggers-RobotRace_left",
        "GoldDiggers_right": "GoldDiggers-RobotRace_right",
        "D3STROYER_main": "D3STROYER_main_tournament",
        "D3STROYER_buddy": "D3STROYER_buddy_tournament",
        "TagTeam": "XAE-12-TagTeam",
        "forsurewinners_main": "forsurewinners",
        "forsurewinners_buddy": "group4",
    }

robotmodules = { m:__import__(m) for m in robot_module_names.values() }

def make_map():
	if args.map is not None:
		return Map.read(args.map)
	return Map.makeRandom(30, 30, args.density)

def vizfile_for_game(game_index):
	if not args.viz:
		return None
	if args.games == 1:
		return args.viz
	root, ext = os.path.splitext(args.viz)
	if not ext:
		ext = ".gif"
	return f"{root}_game_{game_index}{ext}"

def add_players(sim):
	for name,module_name in robot_module_names.items():
		for p in robotmodules[module_name].players:
			p.player_modname = name
			sim.add_player(p)

def final_scoreboard(sim):
	return [
		{
			"player_id": status.player,
			"team": nameFromPlayerId(status.player),
			"team_label": nameFromPlayerId(status.player).upper(),
			"bot": sim._players[idx].player_name,
			"gold": status.gold,
			"health": status.health,
			"position": (status.x, status.y),
		}
		for idx, status in enumerate(sim._status)
	]

def print_game_summary(game_index, scoreboard):
	print("=" * 80)
	print(f"Game {game_index} final scoreboard")
	print("Player             Health   Gold      Position")
	for entry in scoreboard:
		player_label = f"{entry['team_label']} {entry['bot']:<15}"[:17]
		x, y = entry["position"]
		print("{:<17} {:<8} {:<9} {},{}".format(
			player_label,
			entry["health"],
			entry["gold"],
			x,
			y,
		))

	max_gold = max(entry["gold"] for entry in scoreboard)
	winners = [entry for entry in scoreboard if entry["gold"] == max_gold]
	winner_names = ", ".join(
		f"{entry['team_label']} ({entry['bot']})" for entry in winners
	)
	print(f"Winner: {winner_names} with {max_gold} gold")
	return winners

if args.games < 1:
	raise ValueError("--games must be at least 1")
if args.games > 1 and args.map is None:
	raise ValueError("--map is required when using --games so every run uses the same map")

win_counter = Counter()

for game_index in range(1, args.games + 1):
	vizfile = vizfile_for_game(game_index)
	sim = Simulator(map=make_map(), vizfile=vizfile, framerate=args.framerate)
	if args.games > 1:
		sim.printInitial = False
		sim.printRoundBegin = False
		sim.printEvents = False
		sim.printMoves = False
	add_players(sim)
	if args.games > 1:
		with redirect_stdout(io.StringIO()):
			sim.play(rounds=args.number, jumps_allowed=args.allow_jumps, mine_mode=args.mine_mode.lower())
	else:
		sim.play(rounds=args.number, jumps_allowed=args.allow_jumps, mine_mode=args.mine_mode.lower())
	scoreboard = final_scoreboard(sim)
	winners = print_game_summary(game_index, scoreboard)
	for winner in winners:
		win_counter[f"{winner['team_label']} ({winner['bot']})"] += 1

if args.games > 1:
	print("=" * 80)
	print(f"Overall results after {args.games} games")
	for winner_name, wins in win_counter.most_common():
		print(f"{winner_name}: {wins} wins")