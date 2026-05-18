import re
import subprocess
import tempfile
from dataclasses import dataclass
from argparse import ArgumentParser
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerTuple

@dataclass
class StatsRecord:
    player_id: str
    player_name: str
    hp: int
    gold: int
    pos: str
    def __init__(self, cols: list[str]):
        self.player_id = cols[0]
        self.player_name = cols[1]
        self.hp = int(cols[2])
        self.gold = int(cols[3])
        self.pos = cols[4]
    def __repr__(self):
        return f"{self.player_id} {self.player_name} {self.hp} {self.gold} {self.pos}"
    
arg_parser = ArgumentParser(description="Robot Race Monte-Carlo Simulator 7000")
arg_parser.add_argument("-n", "--runs",      help="Number of games to simulate", type=int, default=10)
arg_parser.add_argument("-r", "--rounds",    help="Number of rounds per game",   type=int, default=100)
arg_parser.add_argument("-c", "--chunksize", help="Number of games per chunk",   type=int, default=4)
arg_parser.add_argument("-v", "--viz",       help="Output file (eg. viz.png)",   type=str, default="viz.png")
args = arg_parser.parse_args()


print(f"Simulating {args.runs} runs of {args.rounds} rounds each...")

runs = []
for i in range(args.runs):
    f = tempfile.TemporaryFile(mode='w+')
    p = subprocess.Popen(["python3", "runRobotRace.py", "--number", str(args.rounds)], stdout=f)
    runs.append((p,f))

for i, run in enumerate(runs):
    p,f = run
    p.wait()
    print(f"Run {i+1}/{len(runs)} completed.")

print("All runs completed.")
print("Commencing analysis...")
print("")

numPlayers = -1
numWins = {}
avgGold = {}
results_per_run = []
for i, run in enumerate(runs):
    p,f = run
    f.seek(0)
    results = []
    stats = False
    for line in f:
        if re.match(r"Player\s*Health\s*Gold\s*Position", line):
            stats = True
            numPlayers = 0
            continue
        if re.match(r"Gold Pots:", line):
            stats = False
            continue
        if stats:
            record = StatsRecord(line.split())
            results.append(record)
            numPlayers += 1
            # player_id, player_name, hp, gold, pos = tuple(line.split())

    results_per_run.append(results)

    print(f"Run {i+1}/{len(runs)} analyzed:")
    end_result = results[-numPlayers:]
    winner = max(end_result, key=lambda stat: stat.gold)
    if winner.player_name in numWins:
        numWins[winner.player_name] += 1
    else:
        numWins[winner.player_name] = 1

    print(F"Winner: {winner.player_name}")
    for stat in end_result:
        if stat.player_name in avgGold:
            avgGold[stat.player_name] += stat.gold
        else:
            avgGold[stat.player_name] = stat.gold
        print(stat)
    print("")

for player_name in avgGold.keys():
    avgGold[player_name] //= args.runs

print(f"Number of wins:      {numWins}")
print(f"Average gold at end: {avgGold}")

x = list(range(args.rounds + 2))

# print(y)
# def plot_run(r: int):
    # y = []
color_per_player = [
    '#ff000044',
    '#00ff0044',
    '#0000ff44',
    '#ffff0044',
    '#00ffff44',
    '#ff00ff44',
]
plots_per_player = [[] for p in range(numPlayers)]
for r in range(args.runs):
    gold_per_player  = [[] for p in range(numPlayers)]
    # print(len(results_per_run[r]))
    for i in range(len(results_per_run[r])):
        # y.append(results_per_run[r][i])
        gold_per_player[i % numPlayers].append(results_per_run[r][i])
    # for player_index, y in enumerate(gold_per_player):
    #     plt.plot(x, list(map(lambda stat: stat.gold, y)), label=y[0].player_name)

    for player_index, y in enumerate(gold_per_player):
        plot = plt.plot(x, list(map(lambda stat: stat.gold, y)),
                        label=y[0].player_name,
                        color=color_per_player[player_index])
        plots_per_player[player_index % numPlayers].extend(plot)
        # plots_per_player[player_index % numPlayers].append(plot)
        # print(plot)
        # print(plots_per_player[player_index % numPlayers])
for i, plot in enumerate(plots_per_player):
    plots_per_player[i] = tuple(plot)

# for r in range(args.runs):
    # plot_run(r)
# plot_run(0)


# plt.legend()
# print(plots_per_player)
# print(list(range(len(plots_per_player))))
plt.xlabel("Rounds")
plt.ylabel("Gold")
plt.legend(
    plots_per_player,
    avgGold.keys(),
    # list(range(len(plots_per_player))),
    handler_map={tuple: HandlerTuple(ndivide=None)}
)
plt.savefig(args.viz)
# plt.show()
