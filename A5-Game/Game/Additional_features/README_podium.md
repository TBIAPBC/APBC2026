# Podium Feature

This module provides a **visual podium** for displaying player standings at the end of a game. It is designed to give a fun and clear visualization of the top performers, with special graphics for the top 3 rankings, and a "still showed up" place for 4th.

## What It Does

- Renders a podium PNG showing the top 3 finishers with medals (🥇, 🥈, 🥉) and player avatars.
- Supports custom robot avatars (see below).
- Optionally displays 4th place "on the floor" next to the podium.
- Adds confetti and rich colors for a celebratory atmosphere.
- Dynamically adjusts font-size for names to (hopefully) make sure the names always fit
- Works with any sorted list of (player_name, gold) pairs.

## Usage

All the relevant code is in `podium.py`, which is called in `simulator.py` at the very end of the `play()` function.

To enable the podium simply add the `-p` or `--podium` flag to your run command.

## Custom Avatars

The podium accesses images stored in `APBC2026/A5-Game/Game/Additional_features/bot_imgs/`. Feel free to upload your image to represent your teams bot!

Requirements:
- Has to be a .png file
- Dimensions should be approximately square
- Add the reference by using your bots name + img file name to the `podium.py` `_draw_robot()` function 
- Bots with no custom avatar will use the default img

## Output

- **Podium Display** (displays the final podium using matplotlib)
- **A PNG file** saves podium (as `podium.png` by default, or custom filename) in the current working directory.

## Requirements

- `matplotlib`
- `Pillow` (for image features)

---
