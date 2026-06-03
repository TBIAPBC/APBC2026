# Visualization and Statistics

This add-on provides an improved game visualization and a simple statistics exporter.

## Files
- [A5-Game/Game/illustrator.py](A5-Game/Game/illustrator.py) — renderer and animation generator (draws board, player trails, health colors, gold labels).
- [A5-Game/Game/stats.py](A5-Game/Game/stats.py) — generates comparative per-player plots (gold, health, moves) from simulator statistics.
- [A5-Game/Game/runRobotRace.py](A5-Game/Game/runRobotRace.py) — integrates visualization and the `--stats` flag into the runner.

## Features
- Produces an animation of the match (MP4 preferred) and can fall back to GIF.
- Shows player trails and health-based coloring.
- Displays gold amounts next to robots in gold-colored label boxes. (This could also be a bit annoying mabe a list under the map better let me now)
- Statistics plots use the same matplotlib color cycle as the visual trails so colors match across outputs.

## How to run
- Basic visualization:
```bash
python3 A5-Game/Game/runRobotRace.py --viz output.mp4
```
- With statistics (saves `stats.png` by default):
```bash
python3 A5-Game/Game/runRobotRace.py --viz output.mp4 --stats
```

Common flags:
- `--viz <file>` : filename for visualization (e.g., `output.mp4`)
- `--stats` : generate `stats.png` with per-player series

## Outputs
- Animation file named by `--viz` (MP4 recommended)
- `stats.png` image when `--stats` is used

## Dependencies
- Python packages: `matplotlib`, `numpy`, `pillow` (install with `python3 -m pip install matplotlib numpy pillow`)
- System: `ffmpeg` (required for MP4 output)

## Notes & tips
- If `ffmpeg` is missing the script may fall back to GIF or fail; ensure `ffmpeg` is on `PATH`.
- Large media files are excluded by the repository `.gitignore` (`*.mp4`, `*.png`, `*.gif`).
