import math
import itertools
import matplotlib.pyplot as plt

AVAILABLE_METRICS = [
    ("gold", "Gold per Round", "Gold"),
    ("health", "Health per Round", "Health"),
    ("moves", "Successful Moves per Round", "Moves"),
    ("moves_total", "Total Moves (cumulative)", "Moves"),
    ("wall_crashes", "Wall Crashes per Round", "Crashes"),
    ("player_crashes", "Player Crashes per Round", "Crashes"),
    ("mines_set", "Mines Set per Round", "Mines"),
    ("mines_triggered", "Mines Triggered per Round", "Mines"),
    ("out_of_gold", "Out of Gold Events per Round", "Events"),
    ("out_of_health", "Out of Health Events per Round", "Events"),
]


def plot_stats(sim, filename, plots=None, viz=False):
    """Plot selected per-round statistics for all players.

    If `viz` is True, draw each player's current gold under the plot
    in that player's color (intended for visualization/video frames).
    """
    num_players = len(sim._players)

    if plots is None:
        metrics = AVAILABLE_METRICS
    else:
        metric_lookup = {key: (title, ylabel) for key, title, ylabel in AVAILABLE_METRICS}
        metrics = []
        for key in plots:
            if key not in metric_lookup:
                available = ", ".join(metric_key for metric_key, _, _ in AVAILABLE_METRICS)
                raise ValueError(f"Unknown stats plot '{key}'. Available plots: {available}")
            title, ylabel = metric_lookup[key]
            metrics.append((key, title, ylabel))
        if not metrics:
            raise ValueError("No stats plots selected.")
    
    # Use matplotlib's default color cycle to match the video trails
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = prop_cycle.by_key()['color']
    colors = colors * (num_players // len(colors) + 1)  # repeat if more players than colors
    
    # choose number of columns (1..3) that minimises empty subplots
    max_cols = min(3, len(metrics))
    best = None
    for cols in range(1, max_cols + 1):
        rows = math.ceil(len(metrics) / cols)
        slack = rows * cols - len(metrics)
        if best is None or slack < best[0] or (slack == best[0] and cols > best[1]):
            best = (slack, cols, rows)
    _, ncols, nrows = best
    fig, axes = plt.subplots(nrows, ncols, figsize=(5 * ncols, 4 * nrows), squeeze=False)

    flat_axes = axes.flat
    for ax, (key, title, ylabel) in zip(flat_axes, metrics):
        for pId in range(num_players):
            # support derived cumulative metric for total moves
            if key == 'moves_total':
                per_round = sim.stats[pId].get('moves', [])
                series = list(itertools.accumulate(per_round)) if per_round else []
            else:
                series = sim.stats[pId].get(key, [])

            ax.plot(
                series,
                label=sim._players[pId].player_name,
                color=colors[pId],
                linewidth=2,
            )
        ax.set_title(title, fontsize=14, weight='bold')
        ax.set_xlabel('Round')
        ax.set_ylabel(ylabel)
        ax.legend()
        ax.grid(True, alpha=0.3)

    for ax in list(flat_axes)[len(metrics):]:
        ax.axis('off')
    
    plt.tight_layout()
    plt.savefig(filename, dpi=100)
    print(f"Statistics saved to {filename}")