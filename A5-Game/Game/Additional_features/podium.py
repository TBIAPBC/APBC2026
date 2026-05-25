import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.font_manager import FontProperties
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image
from pathlib import Path

_EMOJI_FONT = FontProperties(family="Segoe UI Emoji")

CONFETTI_COLORS = ["#ff595e", "#ffca3a", "#6a4c93", "#1982c4", "#8ac926", "#ff6b9d", "#ffffff"]
MEDALS = ["🥇", "🥈", "🥉"]

BG_COLOR     = "#1a1a2e"
TEXT_COLOR   = "#1a1a2e"
GOLD_COLOR   = "#e0c040"


def _draw_confetti(ax, n=260, xlim=(-1, 3.6), ylim=(0, 2)):
    xs = [random.uniform(*xlim) for _ in range(n)]
    ys = [random.uniform(*ylim) for _ in range(n)]
    colors = [random.choice(CONFETTI_COLORS) for _ in range(n)]
    sizes  = [random.uniform(10, 60) for _ in range(n)]
    markers = ["*", "o", "s", "D", "^"]
    for x, y, c, s in zip(xs, ys, colors, sizes):
        ax.scatter(x, y, c=c, s=s,
                   marker=random.choice(markers),
                   alpha=random.uniform(0.5, 1.0), zorder=0)


def _draw_robot_img(ax, cx, base_y, img_name):
    script_dir = Path(__file__).resolve().parent
    img_path = script_dir / "bot_imgs" / img_name
    if img_path.exists():
        botImg = Image.open(img_path).convert("RGBA")
    else:
        print(f"Error: Could not find the image at {img_path}")
        print(f"Used Default Img instead")
        # default img as fallback
        img_path = script_dir / "bot_imgs" / "default_bot.png"
        botImg = Image.open(img_path).convert("RGBA")

    orig_w, orig_h = botImg.size
    target_size = 100  # This should align robot images to the graphical scale of podium
    zoom = min(target_size / orig_w, target_size / orig_h)
    #print(f"orig_w: {orig_w}, orig_h: {orig_h}, zoom: {zoom}", img_name)
    im = OffsetImage(botImg, zoom=zoom)
    ab = AnnotationBbox(
        im, (cx, base_y),
        xycoords='data',
        box_alignment=(0.5, 0.0),
        frameon=False
    )
    ax.add_artist(ab)
    return base_y + 0.42  # returns top of robot, base_y + img height

def _draw_robot(ax, cx, base_y, bot_name):
    if bot_name == "GoldDigger-Bot-Basic":
        return _draw_robot_img(ax, cx, base_y, "GoldDiggerBot.png")
    elif bot_name == "NonRandom":
        return _draw_robot_img(ax, cx, base_y, "dice.png")
    #elif bot_name == "YOUR_NAME_HERE":
    #    return _draw_robot_img(ax, cx, base_y, "YOUR_IMG_HERE.png")
    else:
        return _draw_robot_img(ax, cx, base_y, "default_bot.png")
   

def draw_podium(standings, output_file="podium.png"):
    """
    standings: list of (player_name, gold) sorted by gold descending.
    Displays a podium PNG and saves it to output_file.
    """
    top3 = list(standings[:3])
    while len(top3) < 3:
        top3.append(("—", 0))

    # Display order: 2nd left, 1st center, 3rd right
    display = [
        (0, top3[1], 0.6, "#a0a0b0",  MEDALS[1]),
        (1, top3[0], 1.0, "#c8a822",  MEDALS[0]),
        (2, top3[2], 0.4, "#a0634a",  MEDALS[2]),
    ]

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_alpha(1)
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(-1, 3.6)
    ax.set_ylim(0, 2.0)
    ax.axis("off")
    ax.set_title("Final Results", fontsize=35, fontweight="bold",
                 pad=16, color="#f0f0f0")

    _draw_confetti(ax)

    bar_width = 0.75

    for x, (name, gold), h, color, medal in display:
        rect = patches.FancyBboxPatch(
            (x - bar_width / 2, 0), bar_width, h,
            boxstyle="round,pad=0.02",
            facecolor=color, edgecolor="white", linewidth=3.5, zorder=1,
        )
        ax.add_patch(rect)

        ax.text(x, h / 2.2, medal, ha="center", va="center",
                fontsize=22, zorder=2, fontproperties=_EMOJI_FONT)

        robot_top = _draw_robot(ax, x, h, name)

        name_size = max(9, 20 - int((len(name) - 6)*1.4))  # Reduce font size smoothly for longer names
       
        ax.text(x, robot_top - 0.5, name, ha="center", va="center",
                fontsize=name_size, fontweight="bold", color=BG_COLOR, zorder=3)
        ax.text(x, robot_top + 0.15, f"{gold} gold", ha="center", va="center",
                fontsize=10, color=GOLD_COLOR, zorder=3,
                bbox=dict(boxstyle="round,pad=0.3", facecolor=BG_COLOR,
                          edgecolor=GOLD_COLOR, linewidth=1.5))

    # 4th place — standing on the floor, not on the podium
    if len(standings) >= 4:
        name4, gold4 = standings[3]
        robot_top4 = _draw_robot(ax, 2.8, 0, name4)
        name_size = max(9, 20 - int((len(name4) - 6)*1.4)) -2  # Reduce font size smoothly for longer names
        ax.text(2.8, robot_top4 + 0.12, name4, ha="center", va="center",
                fontsize=name_size, fontweight="bold", color="white", zorder=3,
                bbox=dict(boxstyle="round,pad=0.17", facecolor=BG_COLOR,
                          edgecolor="white", linewidth=1.5))
        ax.text(2.8, robot_top4 + 0.25, f"{gold4} gold", ha="center", va="center",
                fontsize=10, color=GOLD_COLOR, zorder=3,
                bbox=dict(boxstyle="round,pad=0.3", facecolor=BG_COLOR,
                          edgecolor=GOLD_COLOR, linewidth=1.5))
        ax.text(3.65, 0.1, "still showed up", ha="right", va="bottom",
                fontsize=16, color="white", zorder=3,
                bbox=dict(boxstyle="round,pad=0.3", facecolor=BG_COLOR,
                          edgecolor="white", linewidth=1.5))

    
    plt.tight_layout()
    plt.savefig(output_file, dpi=120, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.show()
    plt.close()
    print(f"Podium saved to {output_file}")

def draw_podium_from_game_info(game):
    players = game._players
    names = [getattr(p, 'player_name') for p in players]
    golds = [getattr(p.status, 'gold') for p in players]
    standings = sorted(
        zip(names, golds),
        key=lambda x: x[1],
        reverse=True
    )
    draw_podium(standings)
    #draw_podium([('Alice', 500), ('Bob', 320), ('Charlie', 180), ('Diana', 99)])
