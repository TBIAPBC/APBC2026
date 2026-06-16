from game_utils import Direction as D, Map, TileStatus
from player_base import Player
from collections import deque
import math


class StalkerHunterPlayer(Player):
    """
    Adaptive gold-chasing bot with three strategies that activate in sequence.

    Strategies:
        blind_chaser  — default; BFS to chase gold, check competitor paths,
                        and decide whether to chase, wait, or retreat to center.
        camping       — activates after LOSING_STREAK_THRESHOLD consecutive
                        losing pots; stalks the gold and grabs at the last moment.
        rivalry       — activates if camping also fails over STRATEGY_PATIENCE pots;
                        competes directly using ETA-based sprint calculations.

    Transitions:
        blind_chaser → rivalry    if BLIND_CHASER_MAX_ROUNDS is exceeded and
                                  the bot is no longer in 1st place.
        blind_chaser → camping    after LOSING_STREAK_THRESHOLD consecutive losing
                                  pots, or immediately on a RANK_DROP_CAMPING_TRIGGER
                                  rank drop in a single round.
        camping      → rivalry    if average rank over STRATEGY_PATIENCE pots
                                  stays at or below LOSING_RANK_THRESHOLD.
        camping      → rivalry    emergency override when score gap to leader
                                  exceeds RIVALRY_SCORE_MARGIN (is_forced_rivalry).

    Fallback when not chasing:
        - camping / rivalry: move to a spawn-positioning target on the opposite
          side of the map from the current gold, near the center.
        - blind_chaser: retreat toward the map center, then explore frontiers.
    """

    # ---- Movement & Speed ----
    DEFAULT_WALK_SPEED = 3.0
    DEFAULT_SPRINT_SPEED = 7.0
    DEFAULT_SPRINT_RANGE = 7.0
    DEFAULT_AVERAGE_SPEED = 3.0

    # ---- Economy & Profit Margins ----
    MIN_PROFIT_NORMAL = 10
    MIN_PROFIT_RIVALRY = 0
    MAX_ATTRIBUTED_COST_DIST = 7

    # ---- Pathing & Distance Checks ----
    GOLD_PATH_FACTOR = 2.0
    GOLD_PATH_BONUS = 5
    ENEMY_DISTANCE_CUTOFF = 2

    # ---- Sprint Action Moves ----
    NORMAL_BUDGET_DEFAULT_MOVES = 3
    RIVALRY_ETA_SAFETY_MARGIN = 1.0

    # ---- Strategy Triggers & Escalation ----
    LOSING_RANK_THRESHOLD = 2
    LOSING_STREAK_THRESHOLD = 2
    STRATEGY_PATIENCE = 4
    BLIND_CHASER_MAX_ROUNDS = 350
    RANK_DROP_CAMPING_TRIGGER = 2
    RIVALRY_SCORE_MARGIN = 100
    RIVALRY_MAX_RANK = 1

    # ---- Recovery Mode ----
    RECOVERY_LOW_THRESHOLD = 30
    RECOVERY_HIGH_THRESHOLD = 50

    # ---- Camping & Stalking Behavior ----
    STALK_DISTANCE = 1
    MAX_STALK_MOVES = 3

    # ---- Fallback & Positioning Weights ----
    FALLBACK_CURRENT_POS_WEIGHT = 0.4
    FALLBACK_FREE_NEIGHBOR_WEIGHT = 1.0
    FRONTIER_GOLD_DIST_WEIGHT = 0.5
    FALLBACK_MOVES = 2

    # ---- Tracking & Health ----
    LOW_HEALTH_THRESHOLD = 30
    LEADER_HISTORY_MAX_AGE = 200
    STALENESS_PENALTY_WEIGHT = 0.5

    def reset(self, player_id, max_players, width, height):
        """Initialise all per-game state. Called once before each game starts."""
        self.player_name = "StalkerHunter"
        self.ourMap = Map(width, height)
        self.current_enemies = set()
        self.enemy_history = {}
        self.player_id = player_id
        self.max_players = max_players
        self.estimated_scores = {i: 0 for i in range(max_players)}
        self.seen_pots = {}
        self.last_pots = {}
        self.leader_id = None
        self.leader_score = -float('inf')
        self.current_round = 0
        self.center = (width // 2, height // 2)

        self.fallback_target = None
        self.last_gold_pos = None
        self.pot_abandoned = False

        self.active_strategy = "blind_chaser"
        self.pre_recovery_strategy = None
        self.blind_chaser_rounds = 0

        self.pot_gold_id = None
        self.pot_rank_at_spawn = None
        self.pot_score_at_spawn = 0
        self.pot_was_unwinnable = False
        self.pot_spawn_round = 0

        self.losing_streak = 0
        self.last_round_rank = None

        self.camping_pots_played = 0
        self.camping_rank_sum = 0

    def round_begin(self, r):
        """Track the current round number and increment blind_chaser round counter."""
        self.current_round = r
        if self.active_strategy == "blind_chaser":
            self.blind_chaser_rounds += 1

    def set_mines(self, status):
        """No mine placement — returns an empty list."""
        return []

    # ---- Map helpers ----

    def in_bounds(self, x, y):
        """Return True if (x, y) is within the map boundaries."""
        return 0 <= x < self.ourMap.width and 0 <= y < self.ourMap.height

    def is_known_free(self, x, y):
        """Return True if (x, y) is in bounds and confirmed empty on the remembered map."""
        if not self.in_bounds(x, y):
            return False
        return self.ourMap[x, y].status == TileStatus.Empty

    def direction_from_to(self, start_x, start_y, target_x, target_y):
        """Convert two adjacent coordinates into the corresponding Direction enum value."""
        dx, dy = target_x - start_x, target_y - start_y
        for direction in D:
            dir_x, dir_y = direction.as_xy()
            if (dir_x, dir_y) == (dx, dy):
                return direction
        return None

    def count_known_free_neighbors(self, position):
        """Return the number of confirmed-empty tiles directly adjacent to position."""
        x, y = position
        return sum(
            1 for d in D
            if self.is_known_free(x + d.as_xy()[0], y + d.as_xy()[1])
        )

    # ---- Pathfinding ----

    def shortest_path(self, start, goal):
        """
        BFS over the remembered map from start to goal.

        Intermediate tiles must be confirmed empty. The goal tile may be entered
        as long as it is not a known wall. Enemy-occupied tiles are bypassed unless
        they are the goal. Returns a list of (x, y) positions including start and
        goal, or None if no path exists.
        """
        queue = deque([start])
        came_from = {start: None}

        while queue:
            current = queue.popleft()
            if current == goal:
                break
            for direction in D:
                dx, dy = direction.as_xy()
                next_pos = (current[0] + dx, current[1] + dy)

                if next_pos in self.current_enemies and next_pos != goal:
                    continue
                if next_pos in came_from:
                    continue
                if not self.in_bounds(*next_pos):
                    continue
                if next_pos == goal:
                    if self.ourMap[next_pos[0], next_pos[1]].status == TileStatus.Wall:
                        continue
                elif not self.is_known_free(*next_pos):
                    continue

                came_from[next_pos] = current
                queue.append(next_pos)

        if goal not in came_from:
            return None

        path = []
        curr = goal
        while curr is not None:
            path.append(curr)
            curr = came_from[curr]
        path.reverse()
        return path

    def get_visible_enemy_paths(self, status, target):
        """
        Return a list of (player_id, path) pairs for every currently visible enemy,
        where path is the shortest known path from that enemy to target.
        Enemies with no reachable path are omitted.
        """
        paths = []
        for other in status.others:
            if other is None:
                continue
            p = self.shortest_path((other.x, other.y), target)
            if p and len(p) > 1:
                paths.append((other.player, p))
        return paths

    def safe_path_to_moves(self, path, max_moves, enemy_paths):
        """
        Convert a planned path into a list of Direction values, stopping early
        if a future tile would be reached by an enemy before us.

        Contestation is checked per step: if any enemy path passes through the
        next tile at an earlier arrival time than ours, movement stops.
        """
        moves = []
        path_to_walk = path[1:]
        current_node = path[0]

        for i in range(min(max_moves, len(path_to_walk))):
            next_node = path_to_walk[i]
            my_arrival_time = i + 1

            contested = any(
                next_node in e_path and e_path.index(next_node) < my_arrival_time
                for _, e_path in enemy_paths
            )
            if contested:
                break

            direction = self.direction_from_to(
                current_node[0], current_node[1], next_node[0], next_node[1]
            )
            if direction is None:
                break

            moves.append(direction)
            current_node = next_node

        return moves

    # ---- Enemy tracking ----

    def update_enemy_tracker(self, status, gold_pos=None):
        """
        Update per-enemy history with both macro (average speed) and micro
        (burst/sprint capability) tracking.

        Macro data drives Rivalry ETA estimates. Micro data drives Camping
        snatch-prevention checks. Sprint streaks are reset when an enemy
        breaks line of sight for more than one round.
        """
        for other in status.others:
            if other is None:
                continue
            enemy_id = other.player
            current_position = (other.x, other.y)

            if enemy_id not in self.enemy_history:
                self.enemy_history[enemy_id] = {
                    "last_position": current_position,
                    "sprint_speed": self.DEFAULT_SPRINT_SPEED,
                    "walk_speed": self.DEFAULT_WALK_SPEED,
                    "max_sprint_rounds": 1,
                    "current_sprint_streak": 0,
                    "last_seen_round": self.current_round,
                    "total_distance": 0.0,
                    "total_rounds_seen": 0,
                    "average_speed": self.DEFAULT_AVERAGE_SPEED,
                }
            else:
                hist = self.enemy_history[enemy_id]
                last_position = hist["last_position"]
                distance_moved = max(
                    abs(current_position[0] - last_position[0]),
                    abs(current_position[1] - last_position[1]),
                )

                if self.current_round - hist["last_seen_round"] == 1:
                    hist["total_distance"] += distance_moved
                    hist["total_rounds_seen"] += 1
                    hist["average_speed"] = hist["total_distance"] / hist["total_rounds_seen"]

                    if distance_moved > self.DEFAULT_WALK_SPEED:
                        hist["sprint_speed"] = max(hist["sprint_speed"], distance_moved)
                        hist["current_sprint_streak"] += 1
                        hist["max_sprint_rounds"] = max(hist["max_sprint_rounds"], hist["current_sprint_streak"])
                    elif distance_moved > 0:
                        hist["walk_speed"] = max(hist["walk_speed"], distance_moved)
                        hist["current_sprint_streak"] = 0
                else:
                    hist["current_sprint_streak"] = 0

                hist["last_position"] = current_position
                hist["last_seen_round"] = self.current_round

    def calculate_enemy_eta_burst(self, enemy_id, enemy_distance):
        """
        Estimate how many rounds an enemy needs to cover enemy_distance using
        their observed maximum burst (sprint) capability.

        Used by the Camping strategy for short-range snatch-prevention decisions.
        """
        hist = self.enemy_history.get(enemy_id, {})
        sprint_speed = hist.get("sprint_speed", self.DEFAULT_SPRINT_SPEED)
        walk_speed = hist.get("walk_speed", self.DEFAULT_WALK_SPEED)
        max_sprint_rounds = hist.get("max_sprint_rounds", 1)

        max_sprint_distance = sprint_speed * max_sprint_rounds
        if enemy_distance <= max_sprint_distance:
            return enemy_distance / max(1, sprint_speed)

        walk_dist = enemy_distance - max_sprint_distance
        return (max_sprint_distance / max(1, sprint_speed)) + (walk_dist / max(1, walk_speed))

    def calculate_enemy_eta_average(self, enemy_id, enemy_distance):
        """
        Estimate how many rounds an enemy needs to cover enemy_distance using
        their observed long-term average speed.

        Used by the Rivalry strategy and score-attribution for macro-level ETAs.
        """
        hist = self.enemy_history.get(enemy_id, {})
        avg_speed = hist.get("average_speed", self.DEFAULT_AVERAGE_SPEED)
        return enemy_distance / max(1.0, avg_speed)

    # ---- Score estimation ----

    def _attribute_pot(self, pot_pos, pot_value, status):
        """
        Infer which enemy collected a gold pot that has just disappeared.

        First checks if we collected it ourselves (gold increased). Then looks
        for an enemy standing on the exact pot position. Finally falls back to
        ranking all known enemies by estimated ETA to the pot location and
        crediting the fastest one, adjusted for movement cost.

        Returns (winner_player_id, estimated_profit) or (None, 0) if attribution
        fails.
        """
        our_gold_before = (self.pot_score_at_spawn if self.pot_gold_id == pot_pos
                           else self.estimated_scores[self.player_id])
        if status.gold > our_gold_before:
            return None, 0

        for other in status.others:
            if other is None:
                continue
            if (other.x, other.y) == pot_pos:
                return other.player, max(0, pot_value - status.params.cost(1))

        candidates = []
        all_enemy_ids = set(self.enemy_history.keys())
        for other in status.others:
            if other is not None:
                all_enemy_ids.add(other.player)

        for pid in all_enemy_ids:
            if any(o is not None and o.player == pid for o in status.others):
                other = next(o for o in status.others if o is not None and o.player == pid)
                start_pos = (other.x, other.y)
                staleness = 0
            else:
                hist = self.enemy_history.get(pid)
                if hist is None:
                    continue
                start_pos = hist["last_position"]
                staleness = self.current_round - hist.get("last_seen_round", self.current_round)

            path = self.shortest_path(start_pos, pot_pos)
            dist = len(path) - 1 if path is not None else (
                abs(start_pos[0] - pot_pos[0]) + abs(start_pos[1] - pot_pos[1])
            )

            eta = self.calculate_enemy_eta_average(pid, dist) + staleness * self.STALENESS_PENALTY_WEIGHT
            cost = status.params.cost(min(dist, self.MAX_ATTRIBUTED_COST_DIST))
            candidates.append((eta, pid, cost))

        if not candidates:
            enemy_ids = [pid for pid in self.estimated_scores if pid != self.player_id]
            if enemy_ids:
                share = max(0, pot_value) / len(enemy_ids)
                for pid in enemy_ids:
                    self.estimated_scores[pid] += share
            return None, 0

        candidates.sort(key=lambda x: x[0])
        winner_id, cost = candidates[0][1], candidates[0][2]
        return winner_id, max(0, pot_value - cost)

    def update_shadow_scoreboard(self, status):
        """
        Update estimated scores for all players each round.

        Detects pots that disappeared since the last round and attributes them
        via _attribute_pot. Always syncs our own score from the live status.
        Also refreshes leader_id and leader_score.
        """
        if status.goldPots:
            for loc, amount in status.goldPots.items():
                self.seen_pots[loc] = amount

        if self.last_pots:
            for loc, amount in self.last_pots.items():
                if not status.goldPots or loc not in status.goldPots:
                    winner, profit = self._attribute_pot(loc, amount, status)
                    if winner is not None:
                        self.estimated_scores[winner] += profit
                    if loc in self.seen_pots:
                        del self.seen_pots[loc]

        self.estimated_scores[self.player_id] = status.gold
        self.last_pots = status.goldPots.copy() if status.goldPots else {}

        self.leader_id = None
        self.leader_score = -float('inf')
        for pid, score in self.estimated_scores.items():
            if score > self.leader_score:
                self.leader_score = score
                self.leader_id = pid

    def get_my_rank(self):
        """Return our current rank (1 = leading) based on estimated scores."""
        sorted_scores = sorted(self.estimated_scores.items(), key=lambda x: x[1], reverse=True)
        for i, (pid, _) in enumerate(sorted_scores):
            if pid == self.player_id:
                return i + 1
        return self.max_players

    def is_forced_rivalry(self, current_gold):
        """
        Return True if the score gap to the leader is large enough to force
        rivalry mode even while the camping strategy is nominally active.
        """
        return (self.get_my_rank() <= self.RIVALRY_MAX_RANK and
                self.leader_score - current_gold > self.RIVALRY_SCORE_MARGIN)

    # ---- Strategy state machine ----

    def _set_strategy(self, new_strategy):
        """Switch to new_strategy if it differs from the current active strategy."""
        if self.active_strategy != new_strategy:
            self.active_strategy = new_strategy

    def _enter_recovery(self):
        """Pause the current strategy and switch to recovery mode."""
        if self.active_strategy != "recovery":
            self.pre_recovery_strategy = self.active_strategy
            self._set_strategy("recovery")

    def _exit_recovery(self):
        """
        Resume the strategy that was active before recovery began.

        If the previous strategy was blind_chaser, escalate directly to camping
        to avoid re-entering a strategy that already failed at low gold.
        Resets streak and patience counters so the resumed strategy starts fresh.
        """
        resume = self.pre_recovery_strategy or "blind_chaser"
        if resume == "blind_chaser":
            resume = "camping"
        self.pre_recovery_strategy = None
        self._set_strategy(resume)
        self.last_round_rank = self.get_my_rank()
        self.losing_streak = 0
        self.blind_chaser_rounds = 0
        self.camping_pots_played = 0
        self.camping_rank_sum = 0

    def _on_new_pot(self, new_gold_pos, current_score, pot_is_unwinnable=False):
        """
        Called whenever the target gold pot changes.

        Evaluates the outcome of the previous pot (score gained, rank) and
        advances the strategy state machine accordingly. Then resets per-pot
        tracking variables for the new pot.
        """
        current_rank = self.get_my_rank()

        if self.pot_gold_id is not None:
            score_gained = current_score - self.pot_score_at_spawn
            won_pot = score_gained > 0

            if not self.pot_was_unwinnable and self.active_strategy != "recovery":
                end_rank = current_rank

                if self.active_strategy == "blind_chaser":
                    if end_rank >= self.LOSING_RANK_THRESHOLD:
                        self.losing_streak += 1
                    else:
                        self.losing_streak = 0

                    if self.losing_streak >= self.LOSING_STREAK_THRESHOLD:
                        self._set_strategy("camping")
                        self.losing_streak = 0
                        self.camping_pots_played = 0
                        self.camping_rank_sum = 0

                elif self.active_strategy == "camping":
                    self.camping_pots_played += 1
                    self.camping_rank_sum += end_rank

                    if self.camping_pots_played >= self.STRATEGY_PATIENCE:
                        avg_rank = self.camping_rank_sum / self.camping_pots_played
                        if avg_rank >= self.LOSING_RANK_THRESHOLD:
                            self._set_strategy("rivalry")
                        else:
                            self.camping_pots_played = 0
                            self.camping_rank_sum = 0

        self.pot_gold_id = new_gold_pos
        self.pot_score_at_spawn = current_score
        self.pot_rank_at_spawn = current_rank
        self.pot_was_unwinnable = pot_is_unwinnable
        self.pot_spawn_round = self.current_round

    # ---- Winnability ----

    def is_pot_winnable(self, our_dist, enemy_paths, params):
        """
        Return False if any visible enemy is within ENEMY_DISTANCE_CUTOFF tiles
        of the pot AND closer than we are. Otherwise return True.
        """
        if our_dist is None or our_dist == float('inf'):
            return False
        for enemy_id, enemy_path in enemy_paths:
            enemy_dist = len(enemy_path) - 1
            if enemy_dist <= self.ENEMY_DISTANCE_CUTOFF and enemy_dist < our_dist:
                return False
        return True

    # ---- Sprint decisions ----

    def is_gold_path_reasonable(self, position, gold_position, path):
        """
        Return True if the BFS path length is not an excessive detour compared
        to the direct Chebyshev distance to the gold.
        """
        path_length = len(path) - 1
        direct_distance = max(
            abs(gold_position[0] - position[0]),
            abs(gold_position[1] - position[1]),
        )
        return path_length <= direct_distance * self.GOLD_PATH_FACTOR + self.GOLD_PATH_BONUS

    def calculate_sprint_decision_simple(self, path_to_gold, enemy_paths, current_gold, gold_value, params):
        """
        Sprint decision used by the blind_chaser strategy.

        Abandons the pot if an enemy is within ENEMY_DISTANCE_CUTOFF and closer
        than us. Otherwise sprints the full distance if we can afford it and the
        net profit exceeds MIN_PROFIT_NORMAL. Falls back to a conservative
        NORMAL_BUDGET_DEFAULT_MOVES step if not.
        """
        distance_to_gold = len(path_to_gold) - 1
        if distance_to_gold <= 0:
            return True, 0
        closest_enemy_distance = min(
            (len(ep) - 1 for _, ep in enemy_paths),
            default=float("inf")
        )
        if closest_enemy_distance <= self.ENEMY_DISTANCE_CUTOFF and closest_enemy_distance < distance_to_gold:
            return False, 0

        full_sprint_cost = params.cost(distance_to_gold)
        if full_sprint_cost <= current_gold and (gold_value - full_sprint_cost) > self.MIN_PROFIT_NORMAL:
            return True, distance_to_gold
        return True, min(self.NORMAL_BUDGET_DEFAULT_MOVES, distance_to_gold)

    def calculate_sprint_decision(self, path_to_gold, enemy_paths, current_gold, gold_value, rivalry_mode, params):
        """
        Full ETA-based sprint decision used by the camping and rivalry strategies.

        In rivalry mode, enemy ETAs are computed from average speed and the
        distance cutoff is skipped (the ETA math handles it). In camping mode,
        burst ETAs are used and the cutoff applies.

        If an enemy is estimated to arrive before us at normal walk speed, the
        method computes the minimum sprint needed to beat them by
        RIVALRY_ETA_SAFETY_MARGIN rounds. If no enemy is threatening, a greedy
        full sprint is attempted within DEFAULT_SPRINT_RANGE, otherwise the
        default conservative burst is used.
        """
        distance_to_gold = len(path_to_gold) - 1
        if distance_to_gold <= 0:
            return True, 0

        fastest_enemy_eta = float('inf')
        closest_enemy_distance = float('inf')

        for enemy_id, enemy_path in enemy_paths:
            enemy_distance = len(enemy_path) - 1
            if rivalry_mode:
                enemy_eta = self.calculate_enemy_eta_average(enemy_id, enemy_distance)
            else:
                enemy_eta = self.calculate_enemy_eta_burst(enemy_id, enemy_distance)
            if enemy_eta < fastest_enemy_eta:
                fastest_enemy_eta = enemy_eta
            if enemy_distance < closest_enemy_distance:
                closest_enemy_distance = enemy_distance

        if not rivalry_mode:
            if closest_enemy_distance <= self.ENEMY_DISTANCE_CUTOFF and closest_enemy_distance < distance_to_gold:
                return False, 0

        our_normal_eta = distance_to_gold / self.DEFAULT_WALK_SPEED

        if fastest_enemy_eta <= our_normal_eta:
            target_eta = max(1.0, fastest_enemy_eta - self.RIVALRY_ETA_SAFETY_MARGIN)
            desired_moves = min(math.ceil(distance_to_gold / target_eta), distance_to_gold)
            sprint_cost = params.cost(desired_moves)
            eta_rounds = math.ceil(distance_to_gold / max(1, desired_moves))
            decay_penalty = eta_rounds * params.goldPerRound if params.goldDecrease else 0
            expected_profit = (gold_value - decay_penalty) - sprint_cost

            min_profit = self.MIN_PROFIT_RIVALRY if rivalry_mode else self.MIN_PROFIT_NORMAL
            if expected_profit >= min_profit and sprint_cost <= current_gold:
                return True, desired_moves
            return False, 0

        full_sprint_cost = params.cost(distance_to_gold)
        min_profit = self.MIN_PROFIT_RIVALRY if rivalry_mode else self.MIN_PROFIT_NORMAL
        if (distance_to_gold <= self.DEFAULT_SPRINT_RANGE
                and full_sprint_cost <= current_gold
                and (gold_value - full_sprint_cost) >= min_profit):
            return True, distance_to_gold

        return True, min(self.NORMAL_BUDGET_DEFAULT_MOVES, distance_to_gold)

    # ---- Camping helpers ----

    def is_safe_to_wait(self, current_pos, gold_pos, status, my_dist=None):
        """
        Return True if it is safe to keep stalking (hovering near the pot)
        rather than committing to a grab right now.

        Safe means no enemy can reach the pot before we can from STALK_DISTANCE,
        and no enemy can one-round sprint to the pot from their current position.
        """
        if my_dist is None:
            my_path = self.shortest_path(current_pos, gold_pos)
            if not my_path:
                return False
            my_dist = len(my_path) - 1

        my_eta = max(my_dist, self.STALK_DISTANCE) / self.DEFAULT_WALK_SPEED

        for other in status.others:
            if other is None:
                continue
            enemy_path = self.shortest_path((other.x, other.y), gold_pos)
            enemy_dist = len(enemy_path) - 1 if enemy_path else float('inf')
            enemy_sprint_speed = self.enemy_history.get(other.player, {}).get("sprint_speed", self.DEFAULT_SPRINT_SPEED)
            if enemy_dist <= enemy_sprint_speed:
                return False
            if self.calculate_enemy_eta_burst(other.player, enemy_dist) <= my_eta:
                return False
        return True

    def is_gold_in_snatch_danger(self, gold_pos, status):
        """
        Return True if the pot is about to expire or if any enemy could sprint
        to it in one round and has enough gold to afford that sprint.
        """
        if status.goldPotRemainingRounds <= 1:
            return True
        for other in status.others:
            if other is None:
                continue
            enemy_path = self.shortest_path((other.x, other.y), gold_pos)
            if not enemy_path:
                continue
            enemy_dist = len(enemy_path) - 1
            enemy_sprint_speed = self.enemy_history.get(other.player, {}).get("sprint_speed", self.DEFAULT_SPRINT_SPEED)
            if (enemy_dist <= enemy_sprint_speed and
                    self.estimated_scores.get(other.player, 100) >= status.params.cost(enemy_dist)):
                return True
        return False

    # ---- Fallback positioning ----

    def get_fallback_path(self, current_pos):
        """
        Return a path toward the map center for blind_chaser fallback.

        If the center tile is enemy-occupied, the closest unoccupied, non-wall
        tile to the center is chosen instead.
        """
        target = self.center
        if target in self.current_enemies:
            best_candidate = None
            best_dist = float('inf')
            for x in range(self.ourMap.width):
                for y in range(self.ourMap.height):
                    if (x, y) in self.current_enemies or self.ourMap[x, y].status == TileStatus.Wall:
                        continue
                    dist = max(abs(x - self.center[0]), abs(y - self.center[1]))
                    if dist < best_dist:
                        best_dist = dist
                        best_candidate = (x, y)
            if best_candidate:
                target = best_candidate
        return self.shortest_path(current_pos, target)

    def get_predictive_fallback_path(self, current_pos, gold_pos):
        """
        Return a path toward the best repositioning tile for the next gold spawn.

        The target is computed on the opposite side of the map from the current
        gold, near the center. Candidate tiles are scored by distance to that
        target, distance from our current position, and open-ness (free neighbors).
        Used by camping and rivalry strategies.
        """
        center_x, center_y = self.center
        gold_x, gold_y = gold_pos
        away_x, away_y = center_x - gold_x, center_y - gold_y
        target = (
            max(0, min(self.ourMap.width - 1, round(center_x + 0.5 * away_x))),
            max(0, min(self.ourMap.height - 1, round(center_y + 0.5 * away_y))),
        )

        best_candidate, best_score = None, float('inf')
        for x in range(self.ourMap.width):
            for y in range(self.ourMap.height):
                if not self.is_known_free(x, y) or (x, y) in self.current_enemies:
                    continue
                score = (
                    max(abs(x - target[0]), abs(y - target[1]))
                    + self.FALLBACK_CURRENT_POS_WEIGHT * max(abs(x - current_pos[0]), abs(y - current_pos[1]))
                    - self.FALLBACK_FREE_NEIGHBOR_WEIGHT * self.count_known_free_neighbors((x, y))
                )
                if score < best_score:
                    best_score = score
                    best_candidate = (x, y)

        return self.shortest_path(current_pos, best_candidate) if best_candidate else None

    def get_best_frontier_target(self, pos, gold_pos):
        """
        Return a path to the most useful unexplored frontier tile.

        Frontier tiles are confirmed-empty tiles that border at least one unknown
        tile. Candidates are scored by path length plus a weighted penalty for
        distance to the current gold, so exploration still drifts toward the action.
        """
        frontiers = []
        for x in range(self.ourMap.width):
            for y in range(self.ourMap.height):
                if self.ourMap[x, y].status != TileStatus.Empty or (x, y) in self.current_enemies:
                    continue
                for d in D:
                    dx, dy = d.as_xy()
                    nx, ny = x + dx, y + dy
                    if self.in_bounds(nx, ny) and self.ourMap[nx, ny].status == TileStatus.Unknown:
                        frontiers.append((x, y))
                        break

        best_path = None
        best_score = (float('inf'), float('inf'), float('inf'))
        for frontier in frontiers:
            path = self.shortest_path(pos, frontier)
            if path is None or len(path) < 2:
                continue
            dist_to_gold = max(abs(gold_pos[0] - frontier[0]), abs(gold_pos[1] - frontier[1]))
            score = (len(path) - 1 + self.FRONTIER_GOLD_DIST_WEIGHT * dist_to_gold, frontier[0], frontier[1])
            if score < best_score:
                best_score = score
                best_path = path

        return best_path

    # ---- Main orchestrator ----

    def move(self, status):
        """
        Main decision method called every round.

        Execution order:
          1. Update shadow scoreboard and abort if no gold is visible.
          2. Detect a new gold pot and run strategy-transition logic.
          3. Update the remembered map with newly visible tiles.
          4. Return early if health is too low to act.
          5. Refresh enemy positions and tracking history.
          6. Check recovery mode entry/exit.
          7. Resolve the effective strategy (including forced-rivalry override
             and blind_chaser timeout/rank-drop triggers).
          8. Attempt to chase the gold using strategy-specific sprint logic.
          9. If not chasing, move to a fallback/frontier position.
         10. Convert the chosen path to Direction moves via safe_path_to_moves.
        """
        self.update_shadow_scoreboard(status)
        if not status.goldPots:
            return []

        current_gold_pos = min(
            status.goldPots.keys(),
            key=lambda p: max(abs(status.x - p[0]), abs(status.y - p[1]))
        )

        if current_gold_pos != self.pot_gold_id:
            self.pot_abandoned = False
            _our_path = self.shortest_path((status.x, status.y), current_gold_pos)
            _our_dist = len(_our_path) - 1 if _our_path else None
            _spawn_enemy_paths = self.get_visible_enemy_paths(status, current_gold_pos)
            _unwinnable = not self.is_pot_winnable(_our_dist, _spawn_enemy_paths, status.params)
            self._on_new_pot(current_gold_pos, status.gold, pot_is_unwinnable=_unwinnable)

        for x in range(self.ourMap.width):
            for y in range(self.ourMap.height):
                if status.map[x, y].status != TileStatus.Unknown:
                    self.ourMap[x, y].status = status.map[x, y].status

        if status.health < self.LOW_HEALTH_THRESHOLD:
            return []

        current_pos = (status.x, status.y)
        gold_pos = current_gold_pos

        self.current_enemies = set()
        for other in status.others:
            if other is not None:
                self.current_enemies.add((other.x, other.y))

        self.update_enemy_tracker(status, gold_pos)

        if self.active_strategy != "recovery" and status.gold < self.RECOVERY_LOW_THRESHOLD:
            self._enter_recovery()
        elif self.active_strategy == "recovery" and status.gold >= self.RECOVERY_HIGH_THRESHOLD:
            self._exit_recovery()

        effective_strategy = self.active_strategy
        if effective_strategy == "camping" and self.is_forced_rivalry(status.gold):
            effective_strategy = "rivalry"

        current_rank = self.get_my_rank()

        if (self.active_strategy == "blind_chaser"
                and self.blind_chaser_rounds >= self.BLIND_CHASER_MAX_ROUNDS
                and current_rank > 1):
            self._set_strategy("rivalry")
            effective_strategy = "rivalry"
            self.losing_streak = 0
            self.camping_pots_played = 0
            self.camping_rank_sum = 0
        elif (self.active_strategy == "blind_chaser"
                and self.last_round_rank is not None
                and current_rank - self.last_round_rank >= self.RANK_DROP_CAMPING_TRIGGER):
            self._set_strategy("camping")
            effective_strategy = "camping"
            self.losing_streak = 0
            self.camping_pots_played = 0
            self.camping_rank_sum = 0

        self.last_round_rank = current_rank

        path_to_gold = self.shortest_path(current_pos, gold_pos)
        distance_to_gold = len(path_to_gold) - 1 if path_to_gold else float('inf')
        enemy_paths = self.get_visible_enemy_paths(status, gold_pos)

        chasing_gold = False
        num_moves = 0
        best_path = [current_pos]

        if path_to_gold and not self.pot_abandoned:
            gold_value = status.goldPots[gold_pos]

            if effective_strategy == "recovery":
                closest_enemy_distance = min(
                    (len(ep) - 1 for _, ep in enemy_paths),
                    default=float("inf")
                )
                if closest_enemy_distance > 2:
                    chasing_gold = True
                    best_path = path_to_gold
                    num_moves = distance_to_gold
                    while num_moves > 0 and status.params.cost(num_moves) > status.gold:
                        num_moves -= 1
                    if distance_to_gold > 0:
                        num_moves = max(1, num_moves)
                    else:
                        num_moves = 0

            elif effective_strategy == "blind_chaser":
                if distance_to_gold / self.DEFAULT_AVERAGE_SPEED <= status.goldPotRemainingRounds:
                    chasing_gold, num_moves = self.calculate_sprint_decision_simple(
                        path_to_gold, enemy_paths, status.gold, gold_value,
                        params=status.params
                    )
                    if chasing_gold:
                        best_path = path_to_gold

            elif effective_strategy == "rivalry":
                if self.is_gold_path_reasonable(current_pos, gold_pos, path_to_gold):
                    chasing_gold, num_moves = self.calculate_sprint_decision(
                        path_to_gold, enemy_paths, status.gold, gold_value,
                        rivalry_mode=True, params=status.params
                    )
                    if chasing_gold:
                        best_path = path_to_gold

            else:
                if self.is_gold_path_reasonable(current_pos, gold_pos, path_to_gold):
                    if distance_to_gold == 0:
                        chasing_gold = True
                        best_path = path_to_gold
                        num_moves = 0
                    elif distance_to_gold <= self.STALK_DISTANCE:
                        chasing_gold = True
                        best_path = path_to_gold
                        num_moves = distance_to_gold if self.is_gold_in_snatch_danger(gold_pos, status) else 0
                    elif self.is_safe_to_wait(current_pos, gold_pos, status, my_dist=distance_to_gold):
                        chasing_gold = True
                        best_path = path_to_gold
                        num_moves = min(self.MAX_STALK_MOVES, distance_to_gold - self.STALK_DISTANCE)
                    else:
                        chasing_gold, num_moves = self.calculate_sprint_decision(
                            path_to_gold, enemy_paths, status.gold, gold_value,
                            rivalry_mode=False, params=status.params
                        )
                        if chasing_gold:
                            best_path = path_to_gold

            if not chasing_gold:
                self.pot_abandoned = True

        if not chasing_gold:
            if effective_strategy == "recovery":
                return []

            if gold_pos != self.last_gold_pos:
                self.fallback_target = None
                self.last_gold_pos = gold_pos

            if self.fallback_target:
                if current_pos == self.fallback_target:
                    self.fallback_target = None
                elif not self.shortest_path(current_pos, self.fallback_target):
                    self.fallback_target = None

            if not self.fallback_target:
                if effective_strategy in ["camping", "rivalry"]:
                    fp = self.get_predictive_fallback_path(current_pos, gold_pos)
                    if fp and len(fp) > 1:
                        self.fallback_target = fp[-1]
                else:
                    fp = self.get_fallback_path(current_pos)
                    if fp and len(fp) > 1:
                        self.fallback_target = fp[-1]

                    if not self.fallback_target and effective_strategy == "blind_chaser":
                        fp = self.get_best_frontier_target(current_pos, gold_pos)
                        if fp and len(fp) > 1:
                            self.fallback_target = fp[-1]

            if self.fallback_target:
                path_to_fallback = self.shortest_path(current_pos, self.fallback_target)
                if path_to_fallback and len(path_to_fallback) > 1:
                    best_path = path_to_fallback
                    num_moves = self.FALLBACK_MOVES

        target_node = best_path[-1] if best_path else current_pos
        collision_enemy_paths = self.get_visible_enemy_paths(status, target_node)
        return self.safe_path_to_moves(best_path, num_moves, collision_enemy_paths)


players = [StalkerHunterPlayer()]