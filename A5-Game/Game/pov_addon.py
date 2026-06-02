import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap
import numpy as np
import copy
import os

from game_utils import TileStatus


def _mp4_path(path):
    root, ext = os.path.splitext(path)
    if ext.lower() != '.mp4':
        return root + '.mp4'
    return path

class PovRecorder():
    def __init__(self, fileprefix):
        self.pov_data = {}
        self.prefix = fileprefix

    def init_players(self, players):

        for i, player in enumerate(players):
            if hasattr(player, 'ourMap'):
                self.pov_data[i] = {
                    'name': getattr(player, 'player_name', f'player_{i}'),
                    'maps': [],
                    'positions': [],
                    'others': [],
                    'goldpots': [],
                    'health': [],
                    'gold': [],
                }

    def record_round(self, players, goldpots):

        for i, player in enumerate(players):
            if i not in self.pov_data:
                continue
            if not hasattr(player, 'ourMap'):
                continue

            self.pov_data[i]['maps'].append(copy.deepcopy(player.ourMap))
            self.pov_data[i]['positions'].append((player.status.x, player.status.y))
            self.pov_data[i]['goldpots'].append(copy.deepcopy(goldpots))
            self.pov_data[i]['health'].append(player.status.health)
            self.pov_data[i]['gold'].append(player.status.gold)

            visible_others = []
            for other in player.status.others:
                if other is not None:
                    visible_others.append((other.player, other.x, other.y))

            self.pov_data[i]['others'].append(visible_others)
            
    def render_all(self, framerate):
        
        for i, data in self.pov_data.items():
            if len(data['maps']) == 0:
                continue
            filename = os.path.join(f"{self.prefix}_{i}.mp4")
            PovIllustrator(data, filename, framerate).illustrate()

class PovIllustrator:
    
    def __init__(self, pov_data, vizfile, framerate):
        """
        Initialize a PovIllustrator.

        Args:
            pov_data: dictionary containing all data bot has access to
            vizfile: output filename for the generated GIF.
            framerate: frames per second for the animation.

        Side effects:
            Prints a short message announcing the POV being illustrated.
        """
        self.player_name = pov_data['name']
        self.maps = pov_data['maps']
        self.positions = pov_data['positions']
        self.goldpots_history = pov_data['goldpots']
        self.others_history = pov_data['others']
        self.health_history = pov_data['health']
        self.gold_history = pov_data['gold']
        self.vizfile = _mp4_path(vizfile)
        self.frame_per_second = framerate
        self.width = self.maps[0].width
        self.height = self.maps[0].height
        print(f'Illustrating POV for {self.player_name}')
         
    def _map_to_array(self, m):
        """
        Convert a player-local `Map` object into a 2D numpy array of integers.

        The mapping of `TileStatus` to integers is:
            Unknown -> 0, Empty -> 1, Wall -> 2, Mine -> 3

        Args:
            m: a `Map`-like object supporting indexing `m[x, y]` with a `.status` field.

        Returns:
            A numpy array of shape (height, width) with integer codes.
        """
        arr = np.zeros((self.height, self.width), dtype=int)

        for x in range(self.width):
            for y in range(self.height):
                status = m[x, y].status
                if status == TileStatus.Unknown:
                    val = 0
                elif status == TileStatus.Empty:
                    val = 1
                elif status == TileStatus.Wall:
                    val = 2
                elif status == TileStatus.Mine:
                    val = 3
                else:
                    val = 1

                arr[y, x] = val

        return arr

    def illustrate(self):
        """
        Create and save the POV animation as a GIF.

        Builds a matplotlib figure, initializes the first frame from the
        captured maps/positions, then uses `FuncAnimation` to step through
        all rounds and saves the resulting animation to `self.vizfile`.
        """
        fig, self.ax = plt.subplots(figsize=(8, 8))

        self.ax.tick_params(bottom=False, left=False)
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])
        self.ax.set_xlim(-0.5, self.width - 0.5)
        self.ax.set_ylim(-0.5, self.height - 0.5)
        
        self.stats_text = self.ax.text(0.5, -0.08,"",transform=self.ax.transAxes,ha='center',va='top',fontsize=12)

        self.goldpots = self.ax.scatter(x=[], y=[], marker='*', edgecolors='k', c='gold')
        self.others_scatter = self.ax.scatter([], [],marker='X',c='crimson',edgecolors='k', s=100, zorder=2.5)
        
        cmap = ListedColormap([
            '#444444',  # unknown
            '#ffffff',  # empty
            '#111111',  # wall
            '#cc3333',  # mine
        ])

        first = self._map_to_array(self.maps[0])
        self.img = self.ax.imshow(first, cmap=cmap, vmin=0, vmax=3, origin='lower')

        x, y = self.positions[0]
        self.robot = self.ax.scatter([x], [y],marker='D',c='dodgerblue',edgecolors='k', s=120, zorder=3)

        anim = FuncAnimation(fig, self._illustrate_round, frames=len(self.maps))
        anim.save(
            self.vizfile,
            writer='ffmpeg',
            dpi=80,
            fps=self.frame_per_second,
        )
        
    def _illustrate_round(self, i):
        """
        Render a single frame (round `i`) of the POV animation.

        This updates the background map image, the robot marker, gold pot
        markers, the positions of visible other players, and the status text
        (health and gold) for the given round index.

        Args:
            i: integer round index (0-based).
        """
        arr = self._map_to_array(self.maps[i])
        self.img.set_data(arr)

        x, y = self.positions[i]
        self.robot.set_offsets([[x, y]])

        gold_dict = self.goldpots_history[i]
        gold_pos = list(gold_dict.keys())
        gold_amount = list(gold_dict.values())
        self.goldpots.remove() # I had some trouble with goldpots lingering even after the were taken or relocated, so I remove and replace them

        gold_arr = np.array(gold_pos, dtype=float)

        self.goldpots = self.ax.scatter(
            gold_arr[:, 0],
            gold_arr[:, 1],
            marker='*',
            edgecolors='k',
            c='gold',
            s=np.array(gold_amount, dtype=float),
            zorder=2
        )
        
        others = self.others_history[i]
        other_pos = [(x, y) for (_, x, y) in others]

        if other_pos:
            other_arr = np.array(other_pos, dtype=float)
            self.others_scatter.set_offsets(other_arr)
        else:
            self.others_scatter.set_offsets(np.empty((0, 2), dtype=float))
        
        # Title and health/gold status text   
        self.ax.set_title(f"{self.player_name} POV - Round {i+1}", fontsize=16)
        
        health = self.health_history[i]
        gold = self.gold_history[i]

        self.stats_text.set_text(f"Health: {health}   |   Gold: {gold}")
