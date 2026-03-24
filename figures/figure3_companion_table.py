"""
Figure 3 – Companion Detail Table
===================================
A clean, publication-quality reference table listing all six eras with
full columns: Era, Timeframe, Key Milestone, Paradigm Shift, Reference.

Output: output/figure3_companion_table.svg
         output/figure3_companion_table.pdf
"""
import os
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from data import ERA_DATA
from style import PUBLICATION_STYLE, OUTPUT_DIR

plt.rcParams.update(PUBLICATION_STYLE)

# ── Table geometry (normalised 0-1 figure coordinates) ────────────────────────
FIG_W, FIG_H = 14, 8

# Column widths (sum = 1.0 in available span)
COL_WIDTHS = [0.025, 0.14, 0.08, 0.205, 0.305, 0.17]   # id, era, time, milestone, paradigm, ref
COL_KEYS   = ["id", "era_inline", "timeframe", "milestone_inline",
              "paradigm_inline", "reference"]
COL_HEADS  = ["#", "Era", "Timeframe", "Key Milestone",
              "Paradigm Shift", "Key Reference"]

LEFT_MARGIN = 0.03
RIGHT_MARGIN = 0.03
TOP_CONTENT = 0.82     # top of table rows
ROW_H = 0.110          # height per row
HEADER_H = 0.060       # height of header row
CORNER_R = 0.004

# Compute cumulative x positions
_span = 1 - LEFT_MARGIN - RIGHT_MARGIN
_CW = [w * _span for w in COL_WIDTHS]
COL_X = [LEFT_MARGIN + sum(_CW[:i]) for i in range(len(_CW))]


def _draw_cell(ax, x, y, w, h, text, facecolor, text_color,
               fontsize=8.5, bold=False, italic=False,
               ha="left", pad_x=0.008, pad_y=None, multiline=True):
    rect = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={CORNER_R}",
        facecolor=facecolor, edgecolor="white", linewidth=1.5,
        transform=ax.transAxes, zorder=3,
    )
    ax.add_patch(rect)

    if pad_y is None:
        pad_y = h / 2

    tx = x + pad_x if ha == "left" else x + w / 2
    ty = y + pad_y

    kwargs = dict(
        ha=ha, va="center",
        fontsize=fontsize,
        color=text_color,
        transform=ax.transAxes,
        zorder=4,
    )
    if bold:
        kwargs["fontweight"] = "bold"
    if italic:
        kwargs["fontstyle"] = "italic"
    if multiline:
        kwargs["multialignment"] = "left" if ha == "left" else "center"

    ax.text(tx, ty, text, **kwargs)


def make_figure() -> plt.Figure:
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    # ── Title ─────────────────────────────────────────────────────────────────
    fig.text(
        0.5, 0.965,
        "Bacterial Identification Methods — Reference Summary",
        ha="center", va="top",
        fontsize=14, fontweight="bold", color="#1a1a2e",
    )
    fig.text(
        0.5, 0.930,
        "Six eras from Leeuwenhoek's microscope to AI-driven growth phenotyping",
        ha="center", va="top",
        fontsize=9.5, fontstyle="italic", color="#555",
    )

    # ── Header row ────────────────────────────────────────────────────────────
    header_y = TOP_CONTENT
    for j, (head, cx, cw) in enumerate(zip(COL_HEADS, COL_X, _CW)):
        _draw_cell(ax, cx, header_y, cw, HEADER_H,
                   head, facecolor="#1a1a2e", text_color="white",
                   fontsize=9, bold=True,
                   ha="left" if j > 0 else "center",
                   pad_x=0.010 if j > 0 else 0,
                   pad_y=HEADER_H / 2)

    # ── Data rows ─────────────────────────────────────────────────────────────
    for i, era in enumerate(ERA_DATA):
        row_y = TOP_CONTENT - HEADER_H - (i + 1) * ROW_H
        row_bg = era["light"]

        row_values = [era[k] for k in COL_KEYS]

        for j, (val, cx, cw) in enumerate(zip(row_values, COL_X, _CW)):
            if j == 0:
                # ID column: coloured background with era colour
                _draw_cell(ax, cx, row_y, cw, ROW_H,
                           str(val), facecolor=era["color"], text_color="white",
                           fontsize=9, bold=True, ha="center", pad_x=0,
                           pad_y=ROW_H / 2)
            elif j == 1:
                # Era name: slightly darker bg
                _draw_cell(ax, cx, row_y, cw, ROW_H,
                           val, facecolor=era["color"] + "22", text_color=era["color"],
                           fontsize=8.5, bold=True,
                           pad_x=0.008, pad_y=ROW_H / 2)
            else:
                _draw_cell(ax, cx, row_y, cw, ROW_H,
                           val, facecolor=row_bg if i % 2 == 0 else "white",
                           text_color="#222",
                           fontsize=8 if j not in (3, 4) else 7.8,
                           italic=(j == 5),
                           pad_x=0.008, pad_y=ROW_H / 2)

        # Subtle horizontal divider
        div_y = row_y + ROW_H
        ax.plot([LEFT_MARGIN, 1 - RIGHT_MARGIN], [div_y, div_y],
                color="#e0e0e0", lw=0.5, transform=ax.transAxes, zorder=5)

    # ── Outer table border ────────────────────────────────────────────────────
    table_top = TOP_CONTENT + HEADER_H
    table_bot = TOP_CONTENT - HEADER_H - len(ERA_DATA) * ROW_H
    rect = mpatches.FancyBboxPatch(
        (LEFT_MARGIN, table_bot),
        1 - LEFT_MARGIN - RIGHT_MARGIN,
        table_top - table_bot,
        boxstyle="round,pad=0,rounding_size=0.006",
        facecolor="none", edgecolor="#ccc", linewidth=1.5,
        transform=ax.transAxes, zorder=6,
    )
    ax.add_patch(rect)

    # ── Column dividers ───────────────────────────────────────────────────────
    for cx in COL_X[1:]:
        ax.plot([cx, cx], [table_bot, table_top],
                color="#ddd", lw=0.5,
                transform=ax.transAxes, zorder=4)

    # ── Caption ───────────────────────────────────────────────────────────────
    fig.text(
        0.5, 0.015,
        "Table 1. Summary of bacterial identification eras, key milestones, paradigm shifts, and seminal references.",
        ha="center", va="bottom",
        fontsize=8, fontstyle="italic", color="#666",
    )

    fig.tight_layout(rect=[0, 0.02, 1, 0.925])
    return fig


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    fig = make_figure()
    base = os.path.join(OUTPUT_DIR, "figure3_companion_table")
    fig.savefig(base + ".svg")
    fig.savefig(base + ".pdf")
    print(f"Saved {base}.svg and {base}.pdf")
    plt.close(fig)
