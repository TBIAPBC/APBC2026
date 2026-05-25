# POV Add-on — README

## Purpose
This README documents the POV (player-view) add-on: what changed in `simulator.py` and `runRobotRace.py`, what `pov_illustrator.py` does, and how to enable/use the feature.
The feature is meant to make a gif of the player-view for every player that builds an internal map. It's a nice way to keep track of what information is available to your player
at any given time without having to rely on printing statuses and ASCII maps to the terminal.

## Files changed / added
- `simulator.py` — (expanded original) added POV support and hooks to collect per-player data during the run and produce POV animations.
- `runRobotRace.py` - (expanded original) added argument for --pov flag and incuded it to be passed to the Simulator.
- `pov_illustrator.py` — (new) responsible for turning per-player POV snapshots into animated GIFs.

## High-level summary of changes in `simulator.py`
- Constructor: new `pov` parameter (default False). When enabled, the simulator collects per-player POV data.
- New instance attributes: `self.pov` and `self.pov_data` to hold snapshots, positions, health, gold, visible others and goldpots per round.
- New helper methods:
  - `_init_pov_data()` — initializes `self.pov_data` for players that expose `ourMap`.
  - `_record_pov_snapshots()` — called each round to append the player's view, position, gold, health and visible others.
- `play()` now: initializes POV data, calls `_record_pov_snapshots()` each round, and after the simulation creates per-player GIFs using `PovIllustrator` when `self.pov` is True.

## What `pov_illustrator.py` does (summary)
- Accepts lists of player-local Map snapshots and metadata (positions, health, gold, visible others, goldpots) and renders an animated GIF per player showing only what that player saw each round.
- Output files are named `pov_player_{i}.gif` where `i` is the player index.

## How to enable POV during a run
- Use --pov flag to enable tracking of player internal map & additional stats.

After the run you will find `pov_player_0.gif`, `pov_player_1.gif`, ... in the working directory (or the current output folder).

## Notes and caveats
- Only players that expose an internal `ourMap` attribute will have POV data collected; `_init_pov_data()` checks for that.
- POV generation may require image/animation libraries (same as original Illustrator)
- The POV feature collects copies of player-local maps each round; this increases memory usage for long runs or many players. I have not checked it's limits.

## PovIllustrator details

- **Purpose**: Renders a per-player animated GIF showing only the tiles and information that a player saw each round.
- **Constructor arguments**: accepts lists (one entry per round) for `maps`, `positions`, `goldpots`, `others`, `health`, and `gold`, plus `player_name`, an output `vizfile` and `framerate`.
- **Map conversion**: internal helper `_map_to_array()` converts a player-local `Map` into a numpy 2D array. TileStatus maps to integers: Unknown=0, Empty=1, Wall=2, Mine=3.
- **Output**: calls matplotlib's `FuncAnimation` and saves the animation to the provided `vizfile` (e.g., `pov_player_0.gif`).
- **Minimal runtime deps**: `matplotlib`, `numpy` (same as original Illustrator)

