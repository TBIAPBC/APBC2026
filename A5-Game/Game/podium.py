import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.font_manager import FontProperties

_EMOJI_FONT = FontProperties(family="Segoe UI Emoji")

CONFETTI_COLORS = ["#ff595e", "#ffca3a", "#6a4c93", "#1982c4", "#8ac926", "#ff6b9d", "#ffffff"]
MEDALS = ["🥇", "🥈", "🥉"]

BG_COLOR     = "#1a1a2e"
TEXT_COLOR   = "#1a1a2e"
GOLD_COLOR   = "#e0c040"


def _draw_confetti(ax, n=200, xlim=(-0.6, 2.6), ylim=(0, 1.8)):
    xs = [random.uniform(*xlim) for _ in range(n)]
    ys = [random.uniform(*ylim) for _ in range(n)]
    colors = [random.choice(CONFETTI_COLORS) for _ in range(n)]
    sizes  = [random.uniform(10, 60) for _ in range(n)]
    markers = ["*", "o", "s", "D", "^"]
    for x, y, c, s in zip(xs, ys, colors, sizes):
        ax.scatter(x, y, c=c, s=s,
                   marker=random.choice(markers),
                   alpha=random.uniform(0.5, 1.0), zorder=0)


def _draw_robot(ax, cx, base_y):
    hw = 0.075   # body half-width
    bh = 0.13    # body height
    hr = 0.065   # head radius
    er = 0.018   # eye radius

    ax.add_patch(patches.FancyBboxPatch(
        (cx - hw, base_y), 2 * hw, bh,
        boxstyle="round,pad=0.01",
        facecolor="white", edgecolor=BG_COLOR, linewidth=1, zorder=3,
    ))
    ax.add_patch(patches.Circle(
        (cx, base_y + bh + hr), hr,
        facecolor="white", edgecolor=BG_COLOR, linewidth=1, zorder=3,
    ))
    ax.add_patch(patches.Circle((cx - 0.025, base_y + bh + hr), er, facecolor=BG_COLOR, zorder=4))
    ax.add_patch(patches.Circle((cx + 0.025, base_y + bh + hr), er, facecolor=BG_COLOR, zorder=4))
    return base_y + bh + 2 * hr  # returns top of robot


def draw_podium(standings, output_file="podium.png"):
    """
    standings: list of (player_name, gold) sorted by gold descending.
    Saves a podium PNG to output_file.
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
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(-0.6, 3.6)
    ax.set_ylim(0, 2.0)
    ax.axis("off")
    ax.set_title("Final Results", fontsize=35, fontweight="bold",
                 pad=16, color="#f0f0f0")

    _draw_confetti(ax, xlim=(-0.6, 3.6))

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

        robot_top = _draw_robot(ax, x, h)

        ax.text(x, robot_top - 0.35, name, ha="center", va="center",
                fontsize=20, fontweight="bold", color=BG_COLOR, zorder=3)
        ax.text(x, robot_top + 0.15, f"{gold} gold", ha="center", va="center",
                fontsize=10, color=GOLD_COLOR, zorder=3,
                bbox=dict(boxstyle="round,pad=0.3", facecolor=BG_COLOR,
                          edgecolor=GOLD_COLOR, linewidth=1.5))

    # 4th place — standing on the floor, not on the podium
    if len(standings) >= 4:
        name4, gold4 = standings[3]
        robot_top4 = _draw_robot(ax, 2.8, 0)
        ax.text(2.8, robot_top4 + 0.09, name4, ha="center", va="center",
                fontsize=20, fontweight="bold", color="white", zorder=3)
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
    plt.close()
    print(f"Podium saved to {output_file}")


# python -c "from podium import draw_podium; draw_podium([('Alice', 500), ('Bob', 320), ('Charlie', 180)])"
