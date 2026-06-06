# Visualization and Statistics

This document describes the current visualization and statistics behavior in the Robot Race runner.

## Files
- [A5-Game/Game/illustrator.py](A5-Game/Game/illustrator.py): animation renderer (board, trails, robots, mines, gold pots, and bottom labels).
- [A5-Game/Game/stats.py](A5-Game/Game/stats.py): selected per-player stats plotting with optional derived metrics.
- [A5-Game/Game/runRobotRace.py](A5-Game/Game/runRobotRace.py): CLI integration for visualization and stats export.

## Current behavior
- Visualization renders MP4/GIF via matplotlib animation.
- Player trails and stats use a consistent matplotlib color cycle.
- During visualization, each player has a persistent label below the map in the player color.
- Bottom label format is:
	- `PlayerName: current_gold (pots_collected)`
- Stats plotting supports a selectable set of charts via `--stats` short codes.
- A derived cumulative metric is available:
	- `moves_total` (running total of successful moves).

## Stats short codes
Use `--stats` alone for all charts, or pass a short-code string for selected charts.

- `g`: gold
- `h`: health
- `m`: successful moves per round
- `c`: cumulative successful moves (`moves_total`)
- `w`: wall crashes
- `p`: player crashes
- `n`: mines set
- `t`: mines triggered
- `o`: out_of_gold events
- `l`: out_of_health events

Examples:

```bash
# all charts
python3 A5-Game/Game/runRobotRace.py --viz race.mp4 --stats

# selected charts: gold + moves + cumulative moves
python3 A5-Game/Game/runRobotRace.py --viz race.mp4 --stats gmc
```

## Output location
All generated media and plots are saved under:

- `plots/`

Behavior:
- `--viz race.mp4` saves to `plots/race.mp4`
- `--stats` saves to `plots/stats.png`

Only the `plots/` directory is ignored by git (see repository `.gitignore`).

## Dependencies
- Python packages: `matplotlib`, `numpy`, `pillow`
- System package: `ffmpeg` (required for MP4 writing)

Install Python packages with:

```bash
python3 -m pip install matplotlib numpy pillow
```

## Notes
- Unknown `--stats` letters are ignored with a warning.
- If no valid short code is provided, all charts are generated.
