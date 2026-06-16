
# Required dependencies:
- numpy
- matplotlib

### Bring students bots

PR_NUMBER=114
git fetch origin pull/$PR_NUMBER/head:pr-$PR_NUMBER
git merge --no-edit pr-$PR_NUMBER





# 1 - Load dependencies


# 2 - Run the game

cd /Users/agata/Desktop/APBC2026-students-varsion/A5-Game/Game

### Maze 250 solo
```bash
python3 runRobotRace.py --map Maps/maze_map.dat --number 250 --games 100 --viz Tournament/Maze_250_solo/race.gif > Tournament/Maze_250_solo/race_summary.txt
```

### Floodfill 250 solo
```bash
python3 runRobotRace.py --map Maps/floodfill_map.dat --number 250 --games 100  > Tournament/Floodfill_250_solo/race_summary.txt
```

### Maze 1000 solo
```bash
python3 runRobotRace.py --map Maps/maze_map.dat --number 250 --allow_jumps --games 100 --viz Tournament/Maze_1000_solo_jumps/race.mp4 > Tournament/Maze_1000_solo_jumps/race_summary.txt
```





### Maze 250 duet
```bash
python3 runRobotRace_buddy.py --map Maps/maze_map.dat --number 250 --games 50 --viz Tournament/Maze_250_duet/race.mp4  > Tournament/Maze_250_duet/race_summary.txt
```




