#!/usr/bin/env python3
import random
import argparse
from pathlib import Path

from game_utils import nameFromPlayerId
from game_utils import Direction as D, MoveStatus
from game_utils import Tile, TileStatus, TileObject
from game_utils import Map, Status
from simulator import Simulator
from player_base import Player
from stats import plot_stats

def main():

    parser = argparse.ArgumentParser(description="Robot Race Simulator 7000")
    parser.add_argument('--viz', help="filename for the visualization of the race", type=str)
    parser.add_argument('--number', help="number of rounds", type=int, default=1000)
    parser.add_argument('--density', help="map density", type=float, default=0.4)
    parser.add_argument('--framerate', help="specify framerate of the visualization", type=int, default=8)
    parser.add_argument('--map', help="specify map file", type=str,default=None)
    parser.add_argument('--mine_mode', help="specify what mines do. Options are wall, scramble and damage", type=str, default="wall")
    parser.add_argument('--allow_jumps', help="allow players to jump over walls by running into the same direction twice", action=argparse.BooleanOptionalAction)
    parser.add_argument('--theme', type=str, default='default',choices=['default', 'desert', 'forest', 'garden', 'island'])
    parser.add_argument('--pov',  help="filename prefix for pov vizualization. The corresponding player number will always be appended to this prefix", type=str)
    parser.add_argument('-p', '--podium', help="display the podium at the end of the game", action=argparse.BooleanOptionalAction)
    parser.add_argument(
        '--stats',
        help=(
            "generate statistics plots. Optionally provide short codes to select plots, "
            "e.g. '--stats gms' (g=gold, m=moves, h=health, w=wall crashes, p=player crashes, "
            "n=mines set, t=mines triggered, o=out_of_gold, l=out_of_health). "
            "If used without value all plots are generated."
        ),
        nargs='?',
        const='',
        default=None,
    )

    args = parser.parse_args()

    PLOTS_DIR = Path('plots')
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)

    viz_output = None
    if args.viz:
        # Keep only the filename and place visualization outputs under plots/.
        viz_output = str(PLOTS_DIR / Path(args.viz).name)

    robot_module_names = {
        "Test": "test-RobotRace",
        "Beatme": "beatme-RobotRace",
        "GoldDiggers": "GoldDiggers-RobotRace",
        "Adlhartm": "adlhartm-RobotRace",
    }
    robotmodules = { m:__import__(m) for m in robot_module_names.values() }

    if args.map is not None:
        m = Map.read(args.map)
    else:
        m = Map.makeRandom(30, 30, args.density)

    sim = Simulator(
        map=m,
        vizfile=viz_output,
        framerate=args.framerate,
        theme=args.theme,
        povfile=args.pov,
    )

    for name,module_name in robot_module_names.items():
        for p in robotmodules[module_name].players:
            p.player_modname = name
            sim.add_player(p)

    sim.play(rounds=args.number, jumps_allowed=args.allow_jumps, mine_mode=args.mine_mode.lower(), show_podium=args.podium)

    if args.stats is not None:
        # args.stats == '' means flag present without value -> all plots
        plots = None
        if args.stats != '':
            code = args.stats.replace(',', '').replace(' ', '').lower()
            letter_map = {
                'g': 'gold',
                'h': 'health',
                'm': 'moves',
                'w': 'wall_crashes',
                'p': 'player_crashes',
                'n': 'mines_set',
                't': 'mines_triggered',
                'o': 'out_of_gold',
                'l': 'out_of_health',
                    'c': 'moves_total',
            }
            plots = []
            for ch in code:
                if ch in letter_map:
                    key = letter_map[ch]
                    if key not in plots:
                        plots.append(key)
                else:
                    print(f"Warning: unknown stats code '{ch}' - ignoring")
            if not plots:
                print("No valid stats codes provided; generating all plots.")
                plots = None
        plot_stats(sim, str(PLOTS_DIR / 'stats.png'), plots=plots)

if __name__ == "__main__":
    main()