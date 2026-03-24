"""
Figure 2 – Vertical Alternating-Card Timeline
===============================================
A vertical timeline with alternating left/right information cards.
Each era is represented by a coloured circle on the central spine,
with a heading card on alternating sides.

Output: output/figure2_vertical_timeline.svg
         output/figure2_vertical_timeline.pdf
"""
import os
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from data import ERA_DATA
from style import PUBLICATION_STYLE, OUTPUT_DIR

plt.rcParams.update(PUBLICATION_STYLE)

# ── Layout constants ──────────────────────────────────────────────────────────
FIG_W, FIG_H = 12, 16
N = len(ERA_DATA)

SPINE_X = 0.50          # centre spine in figure-fraction x
NODE_R  = 0.025         # node circle radius  (figure-fraction units)
CARD_W  = 0.36          # card width
CARD_H  = 0.110         # card height
CARD_GAP = 0.008        # gap between spine and card edge

# Evenly space nodes vertically (top-to-bottom)
TOP_MARGIN    = 0.93
BOTTOM_MARGIN = 0.04
Y_POSITIONS   = np.linspace(TOP_MARGIN, BOTTOM_MARGIN, N)


def _add_node(ax, x, y, color, num, fig_w, fig_h):
    """Draw a circular node on the spine."""
    # Outer glow ring
    glow = Circle((x, y), NODE_R * 1.35, color=color, alpha=0.18,
                  transform=ax.transAxes, zorder=4)
    ax.add_patch(glow)
    # Main circle
    circle = Circle((x, y), NODE_R, color=color,
                    transform=ax.transAxes, zorder=5)
    ax.add_patch(circle)
    # Number label
    ax.text(x, y, str(num), ha="center", va="center",
            fontsize=10, fontweight="bold", color="white", zorder=6,
            transform=ax.transAxes)


def _add_card(ax, era, y, left_side):
    """Draw an information card on one side of the spine."""
    color = era["color"]
    light = era["light"]

    if left_side:
        card_x = SPINE_X - NODE_R - CARD_GAP - CARD_W
        connector_x0 = card_x + CARD_W
        connector_x1 = SPINE_X - NODE_R
        header_align = "right"
        text_x = card_x + CARD_W - 0.012
    else:
        card_x = SPINE_X + NODE_R + CARD_GAP
        connector_x0 = SPINE_X + NODE_R
        connector_x1 = card_x
        header_align = "left"
        text_x = card_x + 0.012

    # Connector line from node to card
    ax.plot([connector_x0, connector_x1], [y, y],
            color=color, lw=1.4, alpha=0.7,
            transform=ax.transAxes, zorder=3)

    # Card background
    card = FancyBboxPatch(
        (card_x, y - CARD_H / 2),
        CARD_W, CARD_H,
        boxstyle="round,pad=0,rounding_size=0.006",
        facecolor=light, edgecolor=color, linewidth=1.5,
        transform=ax.transAxes, zorder=4,
    )
    ax.add_patch(card)

    # Coloured top-band header
    header_h = 0.032
    header = FancyBboxPatch(
        (card_x, y + CARD_H / 2 - header_h),
        CARD_W, header_h,
        boxstyle="round,pad=0,rounding_size=0.006",
        facecolor=color, edgecolor="none",
        transform=ax.transAxes, zorder=5,
    )
    ax.add_patch(header)

    # Era name in header
    ax.text(
        text_x, y + CARD_H / 2 - header_h / 2,
        era["era_inline"],
        ha=header_align, va="center",
        fontsize=9.5, fontweight="bold", color="white",
        transform=ax.transAxes, zorder=6,
    )

    # Timeframe
    ax.text(
        text_x, y + CARD_H / 2 - header_h - 0.012,
        era["timeframe"],
        ha=header_align, va="top",
        fontsize=8, fontstyle="italic", color=color, fontweight="bold",
        transform=ax.transAxes, zorder=5,
    )

    # Milestone
    ax.text(
        text_x, y,
        "● " + era["milestone_inline"],
        ha=header_align, va="center",
        fontsize=7.8, color="#222",
        transform=ax.transAxes, zorder=5,
        wrap=True,
    )

    # Paradigm shift (smaller, italic, bottom of card)
    ax.text(
        text_x, y - CARD_H / 2 + 0.010,
        era["paradigm_inline"],
        ha=header_align, va="bottom",
        fontsize=7.0, fontstyle="italic", color="#555",
        transform=ax.transAxes, zorder=5,
        wrap=True,
    )


def make_figure() -> plt.Figure:
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    # ── Title ─────────────────────────────────────────────────────────────────
    fig.text(
        0.5, 0.975,
        "Bacterial Identification:\nEvolution of Methods & Paradigm Shifts",
        ha="center", va="top",
        fontsize=14, fontweight="bold", color="#1a1a2e",
        multialignment="center",
    )

    # ── Spine line ────────────────────────────────────────────────────────────
    ax.plot(
        [SPINE_X, SPINE_X],
        [BOTTOM_MARGIN, TOP_MARGIN],
        color="#ccc", lw=2.5, zorder=2,
        transform=ax.transAxes,
        solid_capstyle="round",
    )

    # ── Start / End markers on spine ──────────────────────────────────────────
    for y_mark, label, va in [
        (TOP_MARGIN + 0.01, "1670s", "bottom"),
        (BOTTOM_MARGIN - 0.01, "2025+", "top"),
    ]:
        ax.text(SPINE_X, y_mark, label,
                ha="center", va=va,
                fontsize=8, color="#888", fontstyle="italic",
                transform=ax.transAxes)

    # ── Draw each era ─────────────────────────────────────────────────────────
    for i, (era, y) in enumerate(zip(ERA_DATA, Y_POSITIONS)):
        left = (i % 2 == 0)
        _add_node(ax, SPINE_X, y, era["color"], era["id"], FIG_W, FIG_H)
        _add_card(ax, era, y, left_side=left)

    # ── Paradigm arrow label ───────────────────────────────────────────────────
    ax.annotate(
        "",
        xy=(SPINE_X, BOTTOM_MARGIN - 0.01),
        xytext=(SPINE_X, TOP_MARGIN + 0.01),
        arrowprops=dict(arrowstyle="-|>", color="#aaa", lw=1.5),
        xycoords="axes fraction", textcoords="axes fraction",
        zorder=1,
    )

    # ── Legend / caption ──────────────────────────────────────────────────────
    legend_elements = [
        mpatches.Patch(facecolor=e["color"], label=e["era_inline"])
        for e in ERA_DATA
    ]
    ax.legend(
        handles=legend_elements,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.015),
        ncol=3,
        fontsize=7.5,
        frameon=True,
        edgecolor="#ddd",
        facecolor="#fafafa",
    )

    fig.tight_layout(rect=[0, 0, 1, 0.965])
    return fig


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    fig = make_figure()
    base = os.path.join(OUTPUT_DIR, "figure2_vertical_timeline")
    fig.savefig(base + ".svg")
    fig.savefig(base + ".pdf")
    print(f"Saved {base}.svg and {base}.pdf")
    plt.close(fig)
