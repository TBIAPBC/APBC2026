import matplotlib.pyplot as plt
import matplotlib.patches as patches


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
        (0, top3[1], 0.6, "silver",   "2nd"),
        (1, top3[0], 1.0, "gold",     "1st"),
        (2, top3[2], 0.4, "#cd7f32",  "3rd"),
    ]

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlim(-0.6, 2.6)
    ax.set_ylim(0, 1.8)
    ax.axis("off")
    ax.set_title("Race Results", fontsize=22, fontweight="bold", pad=16)

    bar_width = 0.75

    for x, (name, gold), h, color, place in display:
        rect = patches.FancyBboxPatch(
            (x - bar_width / 2, 0), bar_width, h,
            boxstyle="round,pad=0.02",
            facecolor=color, edgecolor="black", linewidth=1.5,
        )
        ax.add_patch(rect)

        ax.text(x, h / 2, place, ha="center", va="center",
                fontsize=18, fontweight="bold")

        ax.text(x, h + 0.15, name, ha="center", va="center",
                fontsize=11, fontweight="bold")
        ax.text(x, h + 0.05, f"{gold} gold", ha="center", va="center",
                fontsize=9, color="#555555")

    plt.tight_layout()
    plt.savefig(output_file, dpi=120, bbox_inches="tight")
    plt.close()
    print(f"Podium saved to {output_file}")
