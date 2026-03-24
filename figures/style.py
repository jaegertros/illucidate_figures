"""
Shared matplotlib style settings for publication-quality figures.
"""
import matplotlib as mpl

PUBLICATION_STYLE = {
    # Font
    "font.family": "sans-serif",
    "font.sans-serif": ["Lato", "DejaVu Sans", "Liberation Sans"],
    "font.size": 9,
    # Axes
    "axes.titlesize": 13,
    "axes.labelsize": 10,
    "axes.linewidth": 0.8,
    "axes.spines.top": False,
    "axes.spines.right": False,
    # Ticks
    "xtick.major.width": 0.8,
    "ytick.major.width": 0.8,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    # Legend
    "legend.fontsize": 9,
    "legend.frameon": False,
    # Figure
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.1,
    # SVG / PDF text embedding
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    # Lines
    "lines.linewidth": 1.5,
    "patch.linewidth": 0.8,
}

OUTPUT_DIR = "output"
