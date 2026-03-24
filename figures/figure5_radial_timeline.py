"""
Figure 5 – Radial / Circular Timeline
========================================
An alternative, visually striking radial timeline where each era
occupies a sector of a circle. The inner ring shows the era name;
the outer annotation ring shows milestones and paradigm shifts.
Great for presentations and graphical abstracts.

Output: output/figure5_radial_timeline.svg
         output/figure5_radial_timeline.pdf
"""
import os
import sys
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Wedge, FancyBboxPatch
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from data import ERA_DATA
from style import PUBLICATION_STYLE, OUTPUT_DIR

plt.rcParams.update(PUBLICATION_STYLE)

FIG_W, FIG_H = 14, 14
N = len(ERA_DATA)

# Angular parameters (start from top, go clockwise)
START_ANGLE = 90           # degrees, start at top
GAP_DEG     = 4            # gap between sectors
SECTOR_DEG  = (360 - N * GAP_DEG) / N    # each sector's angular span

# Radii (in data units, centre at 0,0)
R_INNER  = 1.0    # inner boundary of sector
R_BAND   = 2.2    # outer boundary of coloured band
R_ICON   = 2.8    # radius for icon circles
R_ANNOT  = 3.6    # radius for annotation text


def _deg_to_rad(d):
    return math.radians(d)


def _sector_angles(i):
    """Return (start, end) in matplotlib convention (CCW from +x)."""
    # Clockwise from top → flip sign
    start = START_ANGLE - i * (SECTOR_DEG + GAP_DEG) - SECTOR_DEG
    end   = START_ANGLE - i * (SECTOR_DEG + GAP_DEG)
    return start, end


def _mid_angle_rad(i):
    start, end = _sector_angles(i)
    return math.radians((start + end) / 2)


def make_figure() -> plt.Figure:
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor("white")

    # ── Centre circle ─────────────────────────────────────────────────────────
    centre = plt.Circle((0, 0), R_INNER - 0.05, color="white", zorder=5)
    ax.add_patch(centre)
    centre_ring = plt.Circle((0, 0), R_INNER - 0.05, fill=False,
                              edgecolor="#ddd", lw=1.5, zorder=6)
    ax.add_patch(centre_ring)

    # Centre text
    ax.text(0, 0.22, "Bacterial\nIdentification",
            ha="center", va="center", fontsize=12, fontweight="bold",
            color="#1a1a2e", multialignment="center", zorder=7)
    ax.text(0, -0.30, "Methods\n1670s → 2025+",
            ha="center", va="center", fontsize=9, fontstyle="italic",
            color="#555", multialignment="center", zorder=7)

    for i, era in enumerate(ERA_DATA):
        start_deg, end_deg = _sector_angles(i)
        mid_rad = _mid_angle_rad(i)
        mid_deg = math.degrees(mid_rad)

        # ── Coloured sector band ──────────────────────────────────────────────
        sector = Wedge(
            (0, 0), R_BAND,
            theta1=start_deg, theta2=end_deg,
            width=R_BAND - R_INNER,
            facecolor=era["color"], edgecolor="white", linewidth=2,
            zorder=3,
        )
        ax.add_patch(sector)

        # ── Light outer arc (annotation background) ───────────────────────────
        outer_arc = Wedge(
            (0, 0), R_ICON + 0.55,
            theta1=start_deg, theta2=end_deg,
            width=0.55,
            facecolor=era["light"], edgecolor=era["color"], linewidth=1,
            zorder=3, alpha=0.85,
        )
        ax.add_patch(outer_arc)

        # ── Era name in sector ────────────────────────────────────────────────
        r_label = (R_INNER + R_BAND) / 2
        lx = r_label * math.cos(mid_rad)
        ly = r_label * math.sin(mid_rad)
        # Rotate text to follow the arc
        rotation = mid_deg if -90 <= mid_deg <= 90 else mid_deg + 180
        ax.text(lx, ly, era["era"],
                ha="center", va="center",
                fontsize=9, fontweight="bold", color="white",
                rotation=rotation, rotation_mode="anchor",
                multialignment="center", zorder=4)

        # ── Era number badge ──────────────────────────────────────────────────
        badge_r_pos = R_INNER + 0.18
        bx = badge_r_pos * math.cos(mid_rad)
        by = badge_r_pos * math.sin(mid_rad)
        badge = plt.Circle((bx, by), 0.17, color="white", zorder=5)
        ax.add_patch(badge)
        ax.text(bx, by, str(era["id"]),
                ha="center", va="center",
                fontsize=9, fontweight="bold", color=era["color"], zorder=6)

        # ── Icon circle ───────────────────────────────────────────────────────
        ix = R_ICON * math.cos(mid_rad)
        iy = R_ICON * math.sin(mid_rad)
        icon_bg = plt.Circle((ix, iy), 0.30, color=era["color"], zorder=4)
        ax.add_patch(icon_bg)
        icon_ring = plt.Circle((ix, iy), 0.30, fill=False,
                                edgecolor="white", lw=1.5, zorder=5)
        ax.add_patch(icon_ring)
        # Icon abbreviation — two-letter shorthand for each era
        abbrev = {
            "microscope":   "Mi",
            "flask":        "Bx",
            "dna":          "16",
            "genome":       "WG",
            "ai":           "AI",
            "growth_curve": "GP",
        }
        ax.text(ix, iy, abbrev.get(era["icon"], str(era["id"])),
                ha="center", va="center",
                fontsize=9.5, fontweight="bold", color="white", zorder=6)

        # ── Milestone annotation ───────────────────────────────────────────────
        ax_label = (R_ICON + 0.55 + 0.55) * math.cos(mid_rad)
        ay_label = (R_ICON + 0.55 + 0.55) * math.sin(mid_rad)
        rotation_annot = mid_deg if -90 <= mid_deg <= 90 else mid_deg + 180

        ax.text(ax_label, ay_label,
                era["timeframe"] + "\n" + era["milestone_inline"],
                ha="center", va="center",
                fontsize=7.5, color=era["color"],
                rotation=rotation_annot, rotation_mode="anchor",
                multialignment="center", zorder=4)

    # ── Outer title ring / frame ───────────────────────────────────────────────
    outer_frame = plt.Circle((0, 0), R_ICON + 1.25, fill=False,
                              edgecolor="#ddd", lw=0.8, zorder=2)
    ax.add_patch(outer_frame)

    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)

    # ── Title & caption ───────────────────────────────────────────────────────
    fig.text(0.5, 0.97,
             "Bacterial Identification — Radial Era Map",
             ha="center", va="top",
             fontsize=14, fontweight="bold", color="#1a1a2e")
    fig.text(0.5, 0.025,
             "Each sector represents one paradigm era. Clockwise from top: Era 1 → Era 6.",
             ha="center", va="bottom",
             fontsize=8.5, fontstyle="italic", color="#666")

    fig.tight_layout(rect=[0, 0.03, 1, 0.96])
    return fig


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    fig = make_figure()
    base = os.path.join(OUTPUT_DIR, "figure5_radial_timeline")
    fig.savefig(base + ".svg")
    fig.savefig(base + ".pdf")
    print(f"Saved {base}.svg and {base}.pdf")
    plt.close(fig)
