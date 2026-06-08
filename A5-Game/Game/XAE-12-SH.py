from game_utils import Direction as D, Map, TileStatus
from player_base import Player
from collections import deque
import math


class StalkerHunterPlayer(Player):
    """
    Adaptive gold-chasing bot with three strategies that activate in sequence.

    Strategies:
        blind_chaser  — default; sprints aggressively for every pot.
        camping       — activates after LOSING_STREAK_THRESHOLD consecutive
                        losing pots; stalks the gold and grabs at the last moment.
        rivalry       — activates if camping also fails over STRATEGY_PATIENCE pots;
                        competes directly using full ETA-based sprint calculations.

    Transitions:
        blind_chaser → rivalry    if the bot has spent 500 rounds in blind_chaser
                                  and is no longer in 1st place.
        blind_chaser → camping    after 3 consecutive losing pots, or immediately
                                  if a single round causes a 2-rank drop.
        camping      → rivalry    if average rank over STRATEGY_PATIENCE pots
                                  remains at or below LOSING_RANK_THRESHOLD.
        camping      → rivalry    emergency override if score gap to leader exceeds
                                  RIVALRY_SCORE_MARGIN (is_forced_rivalry).

    Fallback when not chasing:
        - If a path to gold exists but was declined: move to spawn-positioning
          target (opposite side of map from current gold, near center).
        - If no path to gold exists at all (blind_chaser only): explore toward
          the nearest frontier tile bordering unknown map area.
        Fallback targets are locked for the entire pot lifetime to prevent
        oscillation from round-to-round re-evaluation.
    """

    DEFAULT_WALK_SPEED = 2.0
    DEFAULT_SPRINT_SPEED = 6.0
    DEFAULT_SPRINT_RANGE = 6.0

    HIGH_BUDGET_THRESHOLD = 100
    MIN_PROFIT_NORMAL = 30
    MIN_PROFIT_RIVALRY = 0

    GOLD_PATH_FACTOR = 2.0
    GOLD_PATH_BONUS = 5

    RIVALRY_SCORE_MARGIN = 100
    RIVALRY_MAX_RANK = 1

    STALK_DISTANCE = 1

    LOSING_RANK_THRESHOLD = 3
    LOSING_STREAK_THRESHOLD = 3
    STRATEGY_PATIENCE = 5

    UNWINNABLE_ETA_RATIO = 0.7
    UNWINNABLE_DISTANCE_RATIO = 1

    DISTANCE_CUTOFF = 0.90
    LEADER_HISTORY_MAX_AGE = 5

    def reset(self, player_id, max_players, width, height):
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
        self.blind_chaser_rounds = 0

        self.pot_gold_id = None
        self.pot_rank_at_spawn = None
        self.pot_score_at_spawn = 0
        self.pot_was_unwinnable = False

        self.losing_streak = 0
        self.last_round_rank = None

        self.camping_pots_played = 0
        self.camping_rank_sum = 0

    def round_begin(self, r):
        self.current_round = r
        if self.active_strategy == "blind_chaser":
            self.blind_chaser_rounds += 1

    def set_mines(self, status):
        return []

    # ---- Map helpers ----

    def in_bounds(self, x, y):
        """True if (x, y) lies within the map grid."""
        return 0 <= x < self.ourMap.width and 0 <= y < self.ourMap.height

    def is_known_free(self, x, y):
        """True if (x, y) is in bounds and confirmed empty."""
        if not self.in_bounds(x, y):
            return False
        return self.ourMap[x, y].status == TileStatus.Empty

    def direction_from_to(self, start_x, start_y, target_x, target_y):
        """Return the Direction enum value for a single-step move from start to target, or None."""
        dx, dy = target_x - start_x, target_y - start_y
        for direction in D:
            dir_x, dir_y = direction.as_xy()
            if (dir_x, dir_y) == (dx, dy):
                return direction
        return None

    def count_known_free_neighbors(self, position):
        """Return the number of confirmed-empty tiles adjacent to position."""
        x, y = position
        return sum(
            1 for d in D
            if self.is_known_free(x + d.as_xy()[0], y + d.as_xy()[1])
        )

    # ---- Pathfinding ----

    def shortest_path(self, start, goal):
        """
        BFS over known-free tiles from start to goal.

        Enemy tiles are treated as blocked for intermediate steps but not for
        the goal itself, allowing the bot to path toward a gold tile that an
        enemy is standing on.

        Returns a list of (x, y) positions including start and goal,
        or None if no path exists through currently known tiles.
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
        """Return a list of (player_id, path) for every visible enemy that has a path to target."""
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
        Convert a planned path into a move list, stopping early if any future
        tile would be reached by an enemy at the same time or sooner.

        Returns a (possibly empty) list of Direction values.
        """
        moves = []
        path_to_walk = path[1:]
        current_node = path[0]

        for i in range(min(max_moves, len(path_to_walk))):
            next_node = path_to_walk[i]
            my_arrival_time = i + 1

            contested = any(
                next_node in e_path and e_path.index(next_node) <= my_arrival_time
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
        Update per-enemy history with current position and observed max burst distance.
        Only updates max_burst when the enemy was visible last round (rounds_unseen == 1),
        so teleportation artefacts from off-screen reappearance don't inflate estimates.
        """
        for other in status.others:
            if other is None:
                continue
            enemy_id = other.player
            current_position = (other.x, other.y)

            if enemy_id not in self.enemy_history:
                self.enemy_history[enemy_id] = {
                    "last_position": current_position,
                    "max_burst": self.DEFAULT_SPRINT_SPEED,
                    "last_seen_round": self.current_round,
                }
            else:
                hist = self.enemy_history[enemy_id]
                last_position = hist["last_position"]
                distance_moved = max(
                    abs(current_position[0] - last_position[0]),
                    abs(current_position[1] - last_position[1]),
                )
                if distance_moved > hist.get("max_burst", 0):
                    hist["max_burst"] = distance_moved
                hist["last_position"] = current_position
                hist["last_seen_round"] = self.current_round

    def calculate_enemy_eta(self, enemy_id, enemy_distance):
        """
        Estimate rounds for enemy to reach a tile at enemy_distance steps away.

        Assumes the enemy sprints their observed max_burst tiles at DEFAULT_SPRINT_SPEED,
        then walks the remainder at DEFAULT_WALK_SPEED.
        """
        hist = self.enemy_history.get(enemy_id, {})
        max_burst = hist.get("max_burst", self.DEFAULT_SPRINT_SPEED)

        if enemy_distance <= max_burst:
            return enemy_distance / self.DEFAULT_SPRINT_SPEED
        walk_dist = enemy_distance - max_burst
        return (max_burst / self.DEFAULT_SPRINT_SPEED) + (walk_dist / self.DEFAULT_WALK_SPEED)

    # ---- Score estimation ----

    def _attribute_pot(self, pot_pos, pot_value, status):
        """
        Attribute a disappeared pot to the most likely grabber.

        Priority:
            1. Our gold increased since pot spawn → we grabbed it; return (None, 0)
               so the caller skips enemy attribution.
            2. A visible enemy is standing on the pot tile → certain grab.
            3. Build an ETA-ranked candidate list from all enemies with history,
               including off-screen players using their last known position plus
               a staleness penalty of 0.5 rounds per unseen round.
            4. If no candidates exist, split the value evenly across all enemies
               so gold is not silently lost from the shadow scoreboard.

        Returns (winner_id, net_profit) or (None, 0) if we grabbed it.
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

            eta = self.calculate_enemy_eta(pid, dist) + staleness * 0.5
            cost = status.params.cost(min(dist, 3))
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
        Maintain estimated scores for all players each round.

        Tracks pot appearances and disappearances; attributes disappeared pots
        via _attribute_pot. Our own score is always overwritten with the ground-truth
        value from status.gold. Also updates leader_id and leader_score.
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
        """Return our current rank (1 = first place) based on estimated scores."""
        sorted_scores = sorted(self.estimated_scores.items(), key=lambda x: x[1], reverse=True)
        for i, (pid, _) in enumerate(sorted_scores):
            if pid == self.player_id:
                return i + 1
        return self.max_players

    def is_forced_rivalry(self, current_gold):
        """True if we are dangerously behind the leader and should override camping with rivalry."""
        return (self.get_my_rank() <= self.RIVALRY_MAX_RANK and
                self.leader_score - current_gold > self.RIVALRY_SCORE_MARGIN)

    # ---- Winnability ----

    def is_pot_winnable(self, our_dist, enemy_paths, params):
        """
        False if any visible enemy is both faster and closer than us at full sprint.

        An enemy disqualifies the pot when their ETA is below UNWINNABLE_ETA_RATIO
        of our full-sprint ETA AND their path is at most our distance (structurally
        closer). Requiring both conditions avoids false negatives from fast-but-far
        enemies and false positives from slow-but-close ones.
        """
        if our_dist is None or our_dist == float('inf'):
            return False

        our_sprint_eta = our_dist / self.DEFAULT_SPRINT_SPEED

        for enemy_id, enemy_path in enemy_paths:
            enemy_dist = len(enemy_path) - 1
            enemy_eta = self.calculate_enemy_eta(enemy_id, enemy_dist)
            if (enemy_eta < our_sprint_eta * self.UNWINNABLE_ETA_RATIO and
                    enemy_dist * self.UNWINNABLE_DISTANCE_RATIO <= our_dist):
                return False

        return True

    # ---- Strategy state machine ----

    def _on_new_pot(self, new_gold_pos, current_score, pot_is_unwinnable=False):
        """
        Called once when a new gold pot appears.

        Resolves the previous pot: increments losing_streak or camping counters
        based on end rank, then triggers a strategy escalation if thresholds are
        met. Pots flagged as unwinnable at spawn are excluded from accounting so
        a structurally bad spawn doesn't penalise a working strategy.
        """
        current_rank = self.get_my_rank()

        if self.pot_gold_id is not None and not self.pot_was_unwinnable:
            end_rank = current_rank

            if self.active_strategy == "blind_chaser":
                if end_rank >= self.LOSING_RANK_THRESHOLD:
                    self.losing_streak += 1
                else:
                    self.losing_streak = 0

                if self.losing_streak >= self.LOSING_STREAK_THRESHOLD:
                    self.active_strategy = "camping"
                    self.losing_streak = 0
                    self.camping_pots_played = 0
                    self.camping_rank_sum = 0

            elif self.active_strategy == "camping":
                self.camping_pots_played += 1
                self.camping_rank_sum += end_rank

                if self.camping_pots_played >= self.STRATEGY_PATIENCE:
                    avg_rank = self.camping_rank_sum / self.camping_pots_played
                    if avg_rank >= self.LOSING_RANK_THRESHOLD:
                        self.active_strategy = "rivalry"
                    else:
                        self.camping_pots_played = 0
                        self.camping_rank_sum = 0

        self.pot_gold_id = new_gold_pos
        self.pot_score_at_spawn = current_score
        self.pot_rank_at_spawn = current_rank
        self.pot_was_unwinnable = pot_is_unwinnable

    # ---- Sprint decisions ----

    def is_gold_path_reasonable(self, position, gold_position, path):
        """True if the BFS path length is within GOLD_PATH_FACTOR × direct distance + bonus."""
        path_length = len(path) - 1
        direct_distance = max(
            abs(gold_position[0] - position[0]),
            abs(gold_position[1] - position[1]),
        )
        return path_length <= direct_distance * self.GOLD_PATH_FACTOR + self.GOLD_PATH_BONUS

    def calculate_sprint_decision_simple(self, path_to_gold, enemy_paths, current_gold, gold_value, params):
        """
        Sprint decision for blind_chaser.

        Concedes only if any enemy's path is shorter than DISTANCE_CUTOFF × our distance,
        meaning they are structurally closer. Otherwise always approaches: full sprint if
        profitable, otherwise up to 5 walk moves.

        Returns (should_chase: bool, num_moves: int).
        """
        distance_to_gold = len(path_to_gold) - 1
        if distance_to_gold <= 0:
            return True, 0

        closest_enemy_distance = min(
            (len(ep) - 1 for _, ep in enemy_paths),
            default=float("inf")
        )

        if closest_enemy_distance < distance_to_gold * self.DISTANCE_CUTOFF:
            return False, 0

        full_sprint_cost = params.cost(distance_to_gold)
        if full_sprint_cost <= current_gold and (gold_value - full_sprint_cost) > 30:
            return True, distance_to_gold

        return True, min(5, distance_to_gold)

    def calculate_sprint_decision(self, path_to_gold, enemy_paths, current_gold, gold_value, rivalry_mode, params):
        """
        Sprint decision for camping and rivalry strategies.

        Uses per-enemy ETA estimates to decide whether to sprint and how many moves
        to buy. If an enemy is structurally closer and faster than our full sprint,
        the pot is conceded. Otherwise, buys exactly enough moves to arrive one round
        ahead of the fastest enemy, provided the expected profit meets the minimum
        threshold for the current mode.

        Returns (should_chase: bool, num_moves: int).
        """
        distance_to_gold = len(path_to_gold) - 1
        if distance_to_gold <= 0:
            return True, 0

        fastest_enemy_eta = float('inf')
        closest_enemy_distance = float('inf')

        for enemy_id, enemy_path in enemy_paths:
            enemy_distance = len(enemy_path) - 1
            enemy_eta = self.calculate_enemy_eta(enemy_id, enemy_distance)
            if enemy_eta < fastest_enemy_eta:
                fastest_enemy_eta = enemy_eta
            if enemy_distance < closest_enemy_distance:
                closest_enemy_distance = enemy_distance

        if closest_enemy_distance < distance_to_gold * self.DISTANCE_CUTOFF:
            if fastest_enemy_eta < distance_to_gold / self.DEFAULT_SPRINT_SPEED:
                return False, 0

        our_normal_eta = distance_to_gold / self.DEFAULT_WALK_SPEED

        if fastest_enemy_eta <= our_normal_eta:
            target_eta = max(1.0, fastest_enemy_eta - 1.0)
            desired_moves = min(math.ceil(distance_to_gold / target_eta), distance_to_gold)

            sprint_cost = params.cost(desired_moves)
            eta_rounds = math.ceil(distance_to_gold / max(1, desired_moves))
            decay_penalty = eta_rounds * params.goldPerRound if params.goldDecrease else 0
            expected_profit = (gold_value - decay_penalty) - sprint_cost

            min_profit = self.MIN_PROFIT_RIVALRY if rivalry_mode else self.MIN_PROFIT_NORMAL
            if expected_profit >= min_profit and sprint_cost <= current_gold:
                return True, desired_moves
            return False, 0

        if current_gold > self.HIGH_BUDGET_THRESHOLD and distance_to_gold <= 5:
            return True, distance_to_gold
        if current_gold > self.HIGH_BUDGET_THRESHOLD:
            return True, 4
        return True, min(2, distance_to_gold)

    # ---- Camping helpers ----

    def is_safe_to_wait(self, current_pos, gold_pos, status, my_dist=None):
        """
        True if it is safe to hold position rather than grabbing the gold now.

        Unsafe when any visible enemy is within ceil(their max_burst) tiles of
        the gold (they can one-shot it), or when any enemy's ETA is less than
        or equal to ours (ties go to the enemy).
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

            max_burst = self.enemy_history.get(other.player, {}).get("max_burst", self.DEFAULT_SPRINT_SPEED)
            if enemy_dist <= math.ceil(max_burst):
                return False

            if self.calculate_enemy_eta(other.player, enemy_dist) <= my_eta:
                return False

        return True

    def is_gold_in_snatch_danger(self, gold_pos, status):
        """
        True if we should grab the gold immediately rather than waiting.

        Triggers when the pot expires next round, or when any visible enemy is
        within their burst range and has enough gold to afford the sprint.
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
            max_burst = self.enemy_history.get(other.player, {}).get("max_burst", self.DEFAULT_SPRINT_SPEED)
            if (enemy_dist <= max_burst and
                    self.estimated_scores.get(other.player, 100) >= status.params.cost(enemy_dist)):
                return True

        return False

    # ---- Fallback positioning ----

    def get_fallback_path(self, current_pos, gold_pos):
        """
        Return a path toward the best repositioning tile for the next gold spawn.

        Targets a tile near the center of the map, shifted away from the current
        gold position. Scores candidates by distance to that target, penalised
        slightly for being far from our current position, with a bonus for open
        tiles that offer more future movement options.
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
                    + 0.4 * max(abs(x - current_pos[0]), abs(y - current_pos[1]))
                    - 1.0 * self.count_known_free_neighbors((x, y))
                )
                if score < best_score:
                    best_score = score
                    best_candidate = (x, y)

        return self.shortest_path(current_pos, best_candidate) if best_candidate else None

    def get_best_frontier_target(self, pos, gold_pos):
        """
        Return a path toward the best frontier tile (empty tile bordering unknown area).

        Used by blind_chaser when no path to gold exists, to explore the map toward
        the gold's direction. Scores frontiers by path distance plus half the Chebyshev
        distance to gold. Stable (x, y) tiebreaking prevents oscillation between
        equal-scoring tiles.

        Returns a path list or None if no frontier is reachable.
        """
        frontiers = []
        for x in range(self.ourMap.width):
            for y in range(self.ourMap.height):
                if self.ourMap[x, y].status != TileStatus.Empty:
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
            score = (len(path) - 1 + 0.5 * dist_to_gold, frontier[0], frontier[1])
            if score < best_score:
                best_score = score
                best_path = path

        return best_path

    # ---- Main  ----

    def move(self, status):
        """
        Called every round. Returns a list of Direction values to execute.

        Round structure:
            1. Update shadow scoreboard and map memory.
            2. Detect new gold pot; call _on_new_pot to resolve previous pot and
               advance strategy state machine.
            3. Check for immediate drops in rank to handle emergency transitions.
            4. Phase 1 — Gold pursuit: run the active strategy's chase logic.
               If declined, set pot_abandoned so the decision doesn't flip next round.
            5. Phase 2/3 — Fallback: move to a locked spawn-positioning target
               (or frontier tile if no path to gold exists and strategy is blind_chaser).
               Target is locked for the entire pot lifetime.
            6. Phase 4 — Convert planned path to collision-safe move list.
        """
        self.update_shadow_scoreboard(status)
        if not status.goldPots:
            return []

        current_gold_pos = next(iter(status.goldPots))
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

        if status.health < 30:
            return []

        current_pos = (status.x, status.y)
        gold_pos = next(iter(status.goldPots))

        self.current_enemies = set()
        for other in status.others:
            if other is not None:
                self.current_enemies.add((other.x, other.y))

        self.update_enemy_tracker(status, gold_pos)

        effective_strategy = self.active_strategy
        if effective_strategy == "camping" and self.is_forced_rivalry(status.gold):
            effective_strategy = "rivalry"

        current_rank = self.get_my_rank()
        
        if (self.active_strategy == "blind_chaser"
                and self.blind_chaser_rounds >= 500
                and current_rank > 1):
            self.active_strategy = "rivalry"
            effective_strategy = "rivalry"
            self.losing_streak = 0
            self.camping_pots_played = 0
            self.camping_rank_sum = 0
            
        elif (self.active_strategy == "blind_chaser"
                and self.last_round_rank is not None
                and current_rank - self.last_round_rank >= 2):
            self.active_strategy = "camping"
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

            if effective_strategy == "blind_chaser":
                if distance_to_gold / 5 <= status.goldPotRemainingRounds:
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
                        num_moves = min(2, distance_to_gold - self.STALK_DISTANCE)

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
            if gold_pos != self.last_gold_pos:
                self.fallback_target = None
                self.last_gold_pos = gold_pos

            if self.fallback_target:
                if current_pos == self.fallback_target:
                    self.fallback_target = None
                elif not self.shortest_path(current_pos, self.fallback_target):
                    self.fallback_target = None

            if not self.fallback_target:
                if path_to_gold is not None:
                    fp = self.get_fallback_path(current_pos, gold_pos)
                    if fp and len(fp) > 1:
                        self.fallback_target = fp[-1]
                elif effective_strategy == "blind_chaser":
                    fp = self.get_best_frontier_target(current_pos, gold_pos)
                    if fp and len(fp) > 1:
                        self.fallback_target = fp[-1]

            if self.fallback_target:
                path_to_fallback = self.shortest_path(current_pos, self.fallback_target)
                if path_to_fallback and len(path_to_fallback) > 1:
                    best_path = path_to_fallback
                    num_moves = 2

        target_node = best_path[-1] if best_path else current_pos
        collision_enemy_paths = self.get_visible_enemy_paths(status, target_node)
        return self.safe_path_to_moves(best_path, num_moves, collision_enemy_paths)


players = [StalkerHunterPlayer()]