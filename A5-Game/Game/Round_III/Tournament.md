
cd /Users/agata/Desktop/APBC2026-students-varsion/A5-Game/Game


---

### Test on the normal maze

TEST="Maze_1000"

mkdir -p Round_III/$TEST

python3 runRobotRace.py --map Maps/maze_map.dat --number 1000 --viz race.mp4 --framerate 5 --theme default -p --stats > Round_III/$TEST/race.txt


TEST="Maze_200"

mkdir -p Round_III/$TEST
python3 runRobotRace.py --map Maps/maze_map.dat --number 200 --viz Round_III/$TEST/race.mp4 --framerate 5 --theme default -p --stats > Round_III/$TEST/race.txt


---


### Test on the floodfill

TEST="Floodfill_1000"

mkdir -p Round_III/$TEST

python3 runRobotRace.py --map Maps/floodfill_map.dat --number 1000 --viz race.mp4 --framerate 5 --theme default -p --stats > Round_III/$TEST/race.txt


TEST="Floodfill_200"

mkdir -p Round_III/$TEST
python3 runRobotRace.py --map Maps/floodfill_map.dat --number 200 --viz Round_III/$TEST/race.mp4 --framerate 5 --theme default -p --stats > Round_III/$TEST/race.txt

---

### Test on the mazes_and_caves

TEST="Mazes_and_caves_1000"

mkdir -p Round_III/$TEST

python3 runRobotRace.py --map Maps/mazes_and_caves.dat --number 1000 --viz race.mp4 --framerate 5 --theme default -p --stats > Round_III/$TEST/race.txt


TEST="Mazes_and_caves_200"

mkdir -p Round_III/$TEST
python3 runRobotRace.py --map Maps/mazes_and_caves.dat --number 200 --viz Round_III/$TEST/race.mp4 --framerate 5 --theme default -p --stats > Round_III/$TEST/race.txt



