



#### Basic maze
python3 runRobotRace.py --map Maps/maze_map.dat --number 1000 --viz race.gif --framerate 5 > race.txt

Player             Health   Gold      Position
A 1-GoldDigger     100      1945      20,0
B 2-XAE-12 S3_1    100      2587      22,12        
C 3-D3STROYER      100      1487      21,12
D 4-foreverwinner  100      534       0,24


2:
- good balance between activity and waiting for an opportunity

3:
- very competitive and looks like the most aggressive chaser early on
- it looks like it has issues with overcommiting multi-step turns

1:
- stays inactive for the majority of the game and burst only when the pot is easy to get
- weakest point is "being unlucky" - what if pot never get close or we run shorter simulation?

4:
- seems to be very conservative and apply rarely burst of movements


#### Bottleneck
python3 runRobotRace.py --map Maps/bottleneck_map.dat --number 1000 --viz bottleneck.gif --framerate 5 > bottleneck.txt

Player             Health   Gold      Position
A 1-GoldDigger     100      2814      3,1
B 2-XAE-12 S3_1    100      3641      2,0
C 3-D3STROYER      100      171       22,1
D 4-foreverwinner  100      576       15,25

2:
- it looks like the best “route exploiter”: it keeps moving efficiently through the narrow structure, gets many high-value pots, and stays stable

1:
- becomes much better on this map
- selective burst strategy works better in bottlenecks, where timing and committing at the right moment matter more than constant exploring/wandering

3:
- it definately performs worse on this map
- it's visible that the agressive strategy is costly and a lot of moves are wasted in the narrow corridors
- it is very active, but not efficient

4:
- it mostly plays one-step turns, which is not enough when stronger bots are taking over the critical routes
- on this map you might think slow and careful would help, but here it seems to arrive too late to matter


#### Mazes and caves 
python3 runRobotRace.py --map Maps/mazes_and_caves.dat --number 1000 --viz mazes_and_caves.gif --framerate 5 > mazes_and_caves.txt

Player             Health   Gold      Position
A 1-GoldDigger     100      1587      48,27
B 2-XAE-12 S3_1    100      3367      9,25
C 3-D3STROYER      100      167       28,31
D 4-foreverwinner  100      207       14,37


2:
- clear winner
- it collects gold pots early on and late in the game what is the sign of handling well both, maze navigation and long-run retargeting

1:
- quite decent but inconsistent
- very selective style, no moves for a majority of the rounds and occasional bursts
- it's not the best strategy for this map as many occasions for pot collecting are left out
- another weak point to look at is whether it can really afford a burst that it has planned?

3:
- very active bot it looks it wastes gold for wandering around which is very inefficient on that map
- it's worth checking closely whether moves are not being blocked due to running out of gold/health

4:
- the mostly one-step behavior is too slow to compete for gold consistently
- check whether the distances are calculated as you think they are - what if there are walls?
- maybe being passive before knowing the map of the maze is not the best strategy?


### General tips

Across all maps, the strongest shared success traits are:

- good pot timing
- movement efficiency rather than just movement volume
- adapting burst length to the path and budget
- avoiding failed actions and overcommitting
- being active often enough to colelct pots, but not so active that movement costs eat the profit

The weakest shared traits are:

- passivity that leaves pots uncontested
- overaggression that burns gold on movement
- planning moves that fail because of path conflicts or low gold
- moving too slowly to ever reach contested pots first