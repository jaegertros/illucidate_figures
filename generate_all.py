#!/usr/bin/env python3
"""
generate_all.py
================
Master script — runs all five figure generators and saves SVG + PDF
outputs into the output/ directory.

Usage:
    python generate_all.py

Outputs (in output/):
    figure1_horizontal_timeline.svg / .pdf
    figure2_vertical_timeline.svg   / .pdf
    figure3_companion_table.svg     / .pdf
    figure4_combined.svg            / .pdf
    figure5_radial_timeline.svg     / .pdf
"""
import os
import sys
import importlib
import time

FIGURES_DIR = os.path.join(os.path.dirname(__file__), "figures")
OUTPUT_DIR  = os.path.join(os.path.dirname(__file__), "output")

MODULES = [
    "figure1_horizontal_timeline",
    "figure2_vertical_timeline",
    "figure3_companion_table",
    "figure4_combined",
    "figure5_radial_timeline",
]


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    sys.path.insert(0, FIGURES_DIR)

    # Override the OUTPUT_DIR in child modules so they write to the top-level output/
    import style
    style.OUTPUT_DIR = OUTPUT_DIR

    total = len(MODULES)
    for n, module_name in enumerate(MODULES, 1):
        print(f"[{n}/{total}] Generating {module_name} …", end=" ", flush=True)
        t0 = time.time()

        mod = importlib.import_module(module_name)
        # Refresh module's OUTPUT_DIR reference
        mod.OUTPUT_DIR = OUTPUT_DIR

        fig = mod.make_figure()

        base = os.path.join(OUTPUT_DIR, module_name)
        fig.savefig(base + ".svg")
        fig.savefig(base + ".pdf")

        import matplotlib.pyplot as plt
        plt.close(fig)

        elapsed = time.time() - t0
        print(f"done ({elapsed:.1f}s)")
        print(f"       → {base}.svg")
        print(f"       → {base}.pdf")

    print(f"\n✓ All {total} figures saved to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
