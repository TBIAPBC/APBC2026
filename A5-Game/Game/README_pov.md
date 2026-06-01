# POV Add-on — README

## Purpose
This README documents the POV (player-view) add-on: what changed in `simulator.py` and `runRobotRace.py`, what `pov_addon.py` does, and how to enable/use the feature.

The feature is meant to make a gif of the player-view for every player that builds an internal map. It's a nice way to keep track of what information is available to your player at any given time without having to rely on printing statuses and ASCII maps to the terminal.

## Files changed / added
- `simulator.py` —  gets the string that is used as a prefix for the filename from runRobotRace and initializes PovRecorder when the game starts.
- `runRobotRace.py` - (expanded original) added argument for --pov flag and incuded it to be passed to the Simulator.
- `pov_addon.py` — (new) contains the POV add-on classes:
  - `PovRecorder` for collecting per-player POV data during the simulation
  - `PovIllustrator` for turning recorded POV snapshots into animated GIFs

## High-level summary of changes in `simulator.py`
- initializes PovRecorder at game start.
- `play()` now:
  - initializes players that have internal map.
  - calls `record_round()` from `pov_addon.py` once per round
  - calls `render_all()` from `pov_addon.py` after the simulation to create per-player GIFs when a filename prefix is passed 

## What `pov_addon.py` does (summary)
- `PovRecorder` stores all per-player POV history during the run.
- `PovIllustrator` accepts the recorded data for one player and renders an animated GIF showing only what that player saw each round.
- Output files are named `{prefix}_{i}.gif` by default, where `i` is the player index. And `prefix` is entered by the user.

## `PovRecorder` summary
`PovRecorder` is responsible for collecting and storing the per-round POV data that used to be assembled directly inside the simulator.

It stores, for each tracked player:
- `name`
- `maps`
- `positions`
- `others`
- `goldpots`
- `health`
- `gold`

### Main methods
- `init_players(players)`  
  Initializes POV tracking entries for players that expose an `ourMap` attribute.

- `record_round(players, goldpots)`  
  Called once per round. Records the current player-local map, position, visible others, goldpots, health, and gold.

- `render_all(framerate)`  
  Loops over all recorded player POV histories and passes them to `PovIllustrator` to generate GIFs.

## What `PovIllustrator` does (summary)
- Accepts the recorded POV dictionary for one player and renders an animated GIF per player showing only the information that player had each round.
- Uses matplotlib's `FuncAnimation` to animate the recorded round history.

## How to enable POV during a run
- Use --pov flag to enable tracking of player internal map, it now expects a str that is used as the prefix for the filename.

After the run you will find `{prefix}_0.gif`, `{prefix}_1.gif`, ... in the working directory.

## Notes and caveats
- Only players that expose an internal `ourMap` attribute will have POV data collected; `PovRecorder.init_players()` checks for that.
- POV generation may require image/animation libraries (same as original Illustrator).
- The POV feature collects copies of player-local maps each round; this increases memory usage for long runs or many players. I have not checked its limits.

## PovIllustrator details

- **Purpose**: Renders a per-player animated GIF showing only the tiles and information that a player saw each round.
- **Constructor arguments**: accepts one player's recorded POV dictionary, an output `vizfile` and `framerate`.
- **Map conversion**: internal helper `_map_to_array()` converts a player-local `Map` into a numpy 2D array. TileStatus maps to integers: Unknown=0, Empty=1, Wall=2, Mine=3.
- **Output**: calls matplotlib's `FuncAnimation` and saves the animation to the provided `vizfile` (e.g., `pov_player_0.gif`).
- **Minimal runtime deps**: `matplotlib`, `numpy` (same as original Illustrator)