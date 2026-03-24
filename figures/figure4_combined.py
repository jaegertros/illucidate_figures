"""
Figure 4 – Combined Timeline + Table
======================================
A single publication figure that places a compact horizontal timeline
in the top panel and the full reference table in the bottom panel.
Suitable as a standalone journal figure or slide.

Output: output/figure4_combined.svg
         output/figure4_combined.pdf
"""
import os
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from data import ERA_DATA
from style import PUBLICATION_STYLE, OUTPUT_DIR

plt.rcParams.update(PUBLICATION_STYLE)

FIG_W, FIG_H = 16, 12


def _ribbon_panel(ax):
    """Draw a compact horizontal ribbon into the given axes."""
    N = len(ERA_DATA)
    BLOCK_W = 1.0 / N
    RIB_Y  = 0.50
    RIB_H  = 0.28
    CORNER = 0.012

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # Progression arrow
    arr = FancyArrowPatch(
        (0.01, RIB_Y), (0.99, RIB_Y),
        arrowstyle="-|>", color="#ccc", lw=1.0, mutation_scale=12, zorder=1,
    )
    ax.add_patch(arr)

    for i, era in enumerate(ERA_DATA):
        x0 = i * BLOCK_W + 0.006
        x1 = (i + 1) * BLOCK_W - 0.006
        xc = (x0 + x1) / 2
        above = (i % 2 == 0)

        # Ribbon block
        block = FancyBboxPatch(
            (x0, RIB_Y - RIB_H / 2), x1 - x0, RIB_H,
            boxstyle=f"round,pad=0,rounding_size={CORNER}",
            facecolor=era["color"], edgecolor="white", linewidth=1.8, zorder=3,
        )
        ax.add_patch(block)

        # Era name
        ax.text(xc, RIB_Y + 0.04, era["era"],
                ha="center", va="center",
                fontsize=8, fontweight="bold", color="white", zorder=4,
                multialignment="center")

        # Timeframe below era name
        ax.text(xc, RIB_Y - 0.08, era["timeframe"],
                ha="center", va="center",
                fontsize=7, fontstyle="italic", color="white", zorder=4)

        # Connector tick and milestone label
        tick_y = RIB_Y + RIB_H / 2 if above else RIB_Y - RIB_H / 2
        label_y = tick_y + 0.14 if above else tick_y - 0.14
        ax.plot([xc, xc], [tick_y, label_y - (0.02 if above else -0.02)],
                color=era["color"], lw=0.9, ls="--", zorder=2)
        ax.text(xc, label_y, era["milestone"],
                ha="center", va="bottom" if above else "top",
                fontsize=7, color=era["color"], multialignment="center", zorder=4)

    # "Era" axis label
    ax.text(0.5, 0.01, "← Foundational Methods          Paradigm Progression          Modern Methods →",
            ha="center", va="bottom", fontsize=7.5, color="#999")


# ── Table helpers (reused from figure3) ───────────────────────────────────────
COL_WIDTHS = [0.025, 0.13, 0.075, 0.20, 0.295, 0.17]
COL_KEYS   = ["id", "era_inline", "timeframe", "milestone_inline",
              "paradigm_inline", "reference"]
COL_HEADS  = ["#", "Era", "Timeframe", "Key Milestone",
              "Paradigm Shift", "Key Reference"]
LEFT_M  = 0.02
RIGHT_M = 0.02
CORNER_R = 0.004
ROW_H   = 0.090
HEADER_H = 0.060


def _table_panel(ax):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    span = 1 - LEFT_M - RIGHT_M
    cw = [w * span for w in COL_WIDTHS]
    col_x = [LEFT_M + sum(cw[:i]) for i in range(len(cw))]

    table_top = 0.97
    header_y  = table_top - HEADER_H

    def _cell(x, y, w, h, text, fc, tc, fs=8, bold=False, italic=False, ha="left"):
        rect = FancyBboxPatch(
            (x, y), w, h,
            boxstyle=f"round,pad=0,rounding_size={CORNER_R}",
            facecolor=fc, edgecolor="white", linewidth=1.2,
            transform=ax.transAxes, zorder=3,
        )
        ax.add_patch(rect)
        tx = x + 0.007 if ha == "left" else x + w / 2
        kw = dict(ha=ha, va="center", fontsize=fs, color=tc,
                  transform=ax.transAxes, zorder=4, multialignment="left")
        if bold:   kw["fontweight"] = "bold"
        if italic: kw["fontstyle"] = "italic"
        ax.text(tx, y + h / 2, text, **kw)

    # Header
    for j, (head, cx, cw_j) in enumerate(zip(COL_HEADS, col_x, cw)):
        _cell(cx, header_y, cw_j, HEADER_H, head,
              fc="#1a1a2e", tc="white", fs=8.5, bold=True,
              ha="left" if j > 0 else "center")

    # Rows
    for i, era in enumerate(ERA_DATA):
        ry = header_y - (i + 1) * ROW_H
        vals = [era[k] for k in COL_KEYS]
        for j, (val, cx, cw_j) in enumerate(zip(vals, col_x, cw)):
            if j == 0:
                _cell(cx, ry, cw_j, ROW_H, str(val),
                      fc=era["color"], tc="white", fs=8.5, bold=True, ha="center")
            elif j == 1:
                _cell(cx, ry, cw_j, ROW_H, val,
                      fc=era["color"] + "22", tc=era["color"], fs=8, bold=True)
            else:
                bg = era["light"] if i % 2 == 0 else "white"
                _cell(cx, ry, cw_j, ROW_H, val,
                      fc=bg, tc="#222", fs=7.5, italic=(j == 5))

        ax.plot([LEFT_M, 1 - RIGHT_M], [ry + ROW_H, ry + ROW_H],
                color="#e8e8e8", lw=0.4, transform=ax.transAxes, zorder=5)

    # Outer border
    total_h = HEADER_H + len(ERA_DATA) * ROW_H
    ax.add_patch(mpatches.FancyBboxPatch(
        (LEFT_M, header_y - len(ERA_DATA) * ROW_H),
        1 - LEFT_M - RIGHT_M, total_h,
        boxstyle="round,pad=0,rounding_size=0.005",
        facecolor="none", edgecolor="#ccc", linewidth=1.2,
        transform=ax.transAxes, zorder=6,
    ))


def make_figure() -> plt.Figure:
    fig = plt.figure(figsize=(FIG_W, FIG_H))
    fig.patch.set_facecolor("white")

    # Gridspec: top panel ~35%, bottom panel ~58%, title area ~7%
    gs = fig.add_gridspec(
        2, 1,
        height_ratios=[0.40, 0.60],
        top=0.93, bottom=0.03,
        hspace=0.06,
    )

    ax_top = fig.add_subplot(gs[0])
    ax_bot = fig.add_subplot(gs[1])

    fig.text(
        0.5, 0.975,
        "Bacterial Identification: From Leeuwenhoek to AI-Driven Phenotyping",
        ha="center", va="top",
        fontsize=14, fontweight="bold", color="#1a1a2e",
    )
    fig.text(
        0.5, 0.945,
        "Six historical eras and their defining paradigm shifts",
        ha="center", va="top",
        fontsize=9.5, fontstyle="italic", color="#555",
    )

    _ribbon_panel(ax_top)
    _table_panel(ax_bot)

    # Panel labels
    for ax, label in [(ax_top, "A"), (ax_bot, "B")]:
        ax.text(-0.01, 1.02, label, transform=ax.transAxes,
                fontsize=13, fontweight="bold", color="#1a1a2e")

    return fig


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    fig = make_figure()
    base = os.path.join(OUTPUT_DIR, "figure4_combined")
    fig.savefig(base + ".svg")
    fig.savefig(base + ".pdf")
    print(f"Saved {base}.svg and {base}.pdf")
    plt.close(fig)
