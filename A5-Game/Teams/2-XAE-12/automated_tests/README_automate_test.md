## Usage

The automted.RobotTest.py can run x amount of games with x amount of rounds and keep track of how many moves each robot made on average per game and who was the winner of each game. The final output is an overview of of all game results.

Inside the script at line 30, you can add your robot. The key will be the name used for the result print-out and the value is the file name of your robot without .py

The script_dir is the directory from which the code is being executed. If you plan on moving the automated script, ensure that you change script_dir and robots_dir accordingly at line 36 and 37.

## Adding new robots

If you build your robot in the base Game folder from main, then you need to adjust the import path of your python bot script. Your current imports should be something like this:
- game_utils
- player_base
 - etc.

Please change it to:
- Game.game_utils
- Game.player_base
- etc.

Since the bots are no longer in the same folder as the game import files, the path to the imports has changed. If you choose to make additional subfolders within Robots then keep in mind that all imports must be adjusted accordingly.

The same goes for the imports of your bots. They need to be adjusted to contain Game. before the import.

You can then add your bots to the Robots folder and run the test.

## Execution
```
python automated_RobotTest.py --map Game/Maps/maze_map.dat --number 100 --games 20
```

## Example Result

Starting 20 games silently... Please wait.

--- STATISTICAL ANALYSIS ---

Test_Erratic: 0 wins (0.0%) | Avg Gold: 116.7 | Avg Distance: 95.7 | Avg Moves: 100.0 | Avg Health: 92.3

Beatme_SillyScout: 13 wins (65.0%) | Avg Gold: 266.5 | Avg Distance: 24.9 | Avg Moves: 20.4 | Avg Health: 100.0

Adlhartm_Advanced: 7 wins (35.0%) | Avg Gold: 222.7 | Avg Distance: 307.4 | Avg Moves: 312.5 | Avg Health: 100.0

Draws/Ties: 0 games (0.0%)

