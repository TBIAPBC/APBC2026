import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "Additional_features"))

from game_utils import Map
from simulator import Simulator

bot_module_names = {"Test": "test-RobotRace", "Beatme": "beatme-RobotRace", "GoldDiggers": "GoldDiggers-RobotRace"}
bot_modules = {name: __import__(module) for name, module in bot_module_names.items()}

games = []
for run in range(3):  # 3 rounds
    m = Map.makeRandom(30, 30, 0.4)
    sim = Simulator(map=m, vizfile=None, framerate=8)
    for name, module in bot_modules.items():
        for p in module.players:
            p.player_modname = name
            sim.add_player(p)
    sim.play(rounds=200, jumps_allowed=False, mine_mode="wall")
    games.append(sim)

from podium import draw_podium_from_multi_round
draw_podium_from_multi_round(games, output_file="podium_multi.png")
