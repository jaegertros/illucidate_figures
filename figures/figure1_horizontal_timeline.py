"""
Figure 1 – Horizontal Ribbon Timeline
======================================
A clean, publication-quality horizontal timeline showing the six eras
of bacterial identification. Era blocks are given equal visual width for
clarity; true date spans are shown as text labels on each block.

Output: output/figure1_horizontal_timeline.svg
         output/figure1_horizontal_timeline.pdf
"""
import os
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from data import ERA_DATA
from style import PUBLICATION_STYLE, OUTPUT_DIR

plt.rcParams.update(PUBLICATION_STYLE)

# ── Layout constants ──────────────────────────────────────────────────────────
FIG_W, FIG_H = 18, 8.5          # inches
N = len(ERA_DATA)
BLOCK_W = 1.0 / N               # equal-width blocks in axes fraction
RIBBON_Y = 0.48                 # centre of ribbon in axes coords
RIBBON_H = 0.13                 # height of ribbon
CORNER_R = 0.006                # rounded-corner radius (axes units)

# Vertical offsets for alternating labels
ABOVE_Y = RIBBON_Y + RIBBON_H / 2 + 0.04  # top of connector, odd eras
BELOW_Y = RIBBON_Y - RIBBON_H / 2 - 0.04  # top of connector, even eras
LABEL_H = 0.28                  # height of each label card
LABEL_PAD = 0.012               # padding inside label card


def make_figure() -> plt.Figure:
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    # ── Figure title ──────────────────────────────────────────────────────────
    fig.text(
        0.5, 0.97,
        "Historical Evolution of Bacterial Identification Methods",
        ha="center", va="top",
        fontsize=15, fontweight="bold", color="#1a1a2e",
    )
    fig.text(
        0.5, 0.935,
        "Six paradigm shifts from microscopy (1670s) to AI-driven growth phenotyping (2024–2025)",
        ha="center", va="top",
        fontsize=10, fontstyle="italic", color="#444",
    )

    # ── Arrow across the full ribbon span ─────────────────────────────────────
    arrow = FancyArrowPatch(
        (0.025, RIBBON_Y), (0.978, RIBBON_Y),
        arrowstyle="-|>",
        color="#bbb", lw=1.2,
        mutation_scale=14,
        zorder=1,
    )
    ax.add_patch(arrow)

    for i, era in enumerate(ERA_DATA):
        x0 = i * BLOCK_W + 0.005          # slight gap between blocks
        x1 = (i + 1) * BLOCK_W - 0.005
        xc = (x0 + x1) / 2
        above = (i % 2 == 0)              # odd-index eras go above

        # ── Ribbon block ──────────────────────────────────────────────────────
        ribbon = FancyBboxPatch(
            (x0, RIBBON_Y - RIBBON_H / 2),
            x1 - x0,
            RIBBON_H,
            boxstyle=f"round,pad=0,rounding_size={CORNER_R}",
            facecolor=era["color"],
            edgecolor="white",
            linewidth=2.0,
            zorder=3,
        )
        ax.add_patch(ribbon)

        # Era number badge
        badge_r = 0.018
        badge = plt.Circle(
            (x0 + badge_r + 0.006, RIBBON_Y),
            badge_r,
            color="white", zorder=5, transform=ax.transAxes, clip_on=False,
        )
        ax.add_patch(badge)
        ax.text(
            x0 + badge_r + 0.006, RIBBON_Y,
            str(era["id"]),
            ha="center", va="center",
            fontsize=7.5, fontweight="bold",
            color=era["color"], zorder=6,
            transform=ax.transAxes,
        )

        # Era name inside ribbon
        ax.text(
            xc + 0.012, RIBBON_Y,
            era["era"],
            ha="center", va="center",
            fontsize=8.5, fontweight="bold",
            color="white", zorder=4,
            transform=ax.transAxes,
            multialignment="center",
        )

        # ── Connector line ─────────────────────────────────────────────────────
        if above:
            conn_y0 = RIBBON_Y + RIBBON_H / 2
            conn_y1 = 1 - 0.04 - LABEL_H
            card_y  = conn_y1
        else:
            conn_y0 = RIBBON_Y - RIBBON_H / 2
            conn_y1 = 0.04 + LABEL_H
            card_y  = 0.04

        ax.plot(
            [xc, xc], [conn_y0, conn_y1],
            color=era["color"], lw=1.2, ls="--",
            zorder=2, transform=ax.transAxes,
        )

        # ── Label card ────────────────────────────────────────────────────────
        card_x = x0 + 0.003
        card = FancyBboxPatch(
            (card_x, card_y),
            x1 - x0 - 0.006,
            LABEL_H,
            boxstyle=f"round,pad=0,rounding_size={CORNER_R}",
            facecolor=era["light"],
            edgecolor=era["color"],
            linewidth=1.2,
            zorder=3,
            transform=ax.transAxes,
        )
        ax.add_patch(card)

        # Timeframe
        ax.text(
            xc, card_y + LABEL_H - LABEL_PAD,
            era["timeframe"],
            ha="center", va="top",
            fontsize=7.5, fontstyle="italic",
            color=era["color"], fontweight="bold",
            zorder=4, transform=ax.transAxes,
        )

        # Milestone
        ax.text(
            xc, card_y + LABEL_H / 2 + 0.005,
            era["milestone"],
            ha="center", va="center",
            fontsize=7.5,
            color="#222",
            zorder=4, transform=ax.transAxes,
            multialignment="center",
        )

        # Paradigm shift separator
        sep_y = card_y + 0.068
        ax.plot(
            [card_x + 0.005, card_x + (x1 - x0 - 0.006) - 0.005],
            [sep_y, sep_y],
            color=era["color"], lw=0.6, alpha=0.5,
            transform=ax.transAxes, zorder=4,
        )

        # Paradigm label
        ax.text(
            xc, card_y + LABEL_PAD * 3,
            era["paradigm"],
            ha="center", va="bottom",
            fontsize=6.8, fontstyle="italic",
            color="#555",
            zorder=4, transform=ax.transAxes,
            multialignment="center",
        )

        # ── Timeframe on ribbon ───────────────────────────────────────────────
        ax.text(
            xc, RIBBON_Y - RIBBON_H / 2 - 0.015,
            era["timeframe"],
            ha="center", va="top",
            fontsize=6.5, color="#666",
            zorder=4, transform=ax.transAxes,
        )

    # ── "PARADIGM SHIFT →" progression label ─────────────────────────────────
    ax.text(
        0.5, 0.015,
        "← Earlier Approaches      Paradigm Progression      Modern Methods →",
        ha="center", va="bottom",
        fontsize=8, color="#888",
        transform=ax.transAxes,
    )

    fig.tight_layout(rect=[0, 0.02, 1, 0.93])
    return fig


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    fig = make_figure()
    base = os.path.join(OUTPUT_DIR, "figure1_horizontal_timeline")
    fig.savefig(base + ".svg")
    fig.savefig(base + ".pdf")
    print(f"Saved {base}.svg and {base}.pdf")
    plt.close(fig)
