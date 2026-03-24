# illucidate_figures

Publication-quality timeline figures and SVG icons illustrating the historical
evolution of bacterial identification methods — from Leeuwenhoek's microscope
(1670s) to AI-driven growth phenotyping (2024–2025).

---

## Figures

Five distinct visual approaches are provided so the best fit can be chosen for
a paper, thesis, slide deck, or graphical abstract.

| # | File | Description | Size |
|---|------|-------------|------|
| 1 | `figure1_horizontal_timeline` | **Horizontal ribbon** — six coloured era blocks on a single horizontal axis with alternating above/below label cards | 18 × 8.5 in |
| 2 | `figure2_vertical_timeline`   | **Vertical alternating-card** — classic two-column spine layout with rich detail cards | 12 × 16 in |
| 3 | `figure3_companion_table`     | **Companion reference table** — full six-row colour-coded table (Era · Timeframe · Milestone · Paradigm Shift · Reference) | 14 × 8 in |
| 4 | `figure4_combined`            | **Combined A/B** — ribbon timeline (panel A) above reference table (panel B) in one figure | 16 × 12 in |
| 5 | `figure5_radial_timeline`     | **Radial era map** — circular sector arrangement, ideal for graphical abstracts and presentations | 14 × 14 in |

All figures are exported as **SVG** (fully editable vectors, text as text) and **PDF** (print-ready with embedded fonts).

---

## SVG Icons

Six standalone vector icons — one per era — live in `icons/`.  
They use monochrome line art matching each era's accent colour and are designed
to be embedded in figures or used independently.

| Icon file | Era | Colour |
|-----------|-----|--------|
| `icon_microscope.svg` | Observation & Morphology | `#5B4A8A` |
| `icon_flask.svg` | Biochemical Profiling | `#1B7B8A` |
| `icon_dna.svg` | 16S rRNA Revolution | `#2D8C5A` |
| `icon_genome.svg` | Genomic Resolution | `#C87A20` |
| `icon_ai.svg` | High-Dimensional AI | `#2155A0` |
| `icon_growth_curve.svg` | Dynamic Phenotyping | `#8B3A9B` |

---

## The Six Eras

| # | Era | Timeframe | Key Milestone | Paradigm Shift |
|---|-----|-----------|---------------|----------------|
| 1 | Observation & Morphology | 1670s – 1880s | Microscopy, pure culture, & Gram staining | Established visual characteristics and fundamental classification logic |
| 2 | Biochemical Profiling | Mid-1900s | Metabolic screening (fermentation, catalase) | Shifted focus from static morphology to active metabolic phenotypes |
| 3 | 16S rRNA Revolution | 1970s – 2000s | Phylogeny via 16S rRNA sequencing | Replaced phenotypic approximation with exact genotypic ID; unlocked unculturable taxa |
| 4 | Genomic Resolution | 2010s | Whole Genome Sequencing (WGS) | Moved from single-gene ID to single-base, strain-level genomic resolution |
| 5 | High-Dimensional AI | 2020s+ | ML-driven classification & clustering | Transitioned from human-led sequence analysis to AI-driven pattern recognition |
| 6 | Dynamic Phenotyping | 2024 – 2025 | AI models on growth kinetics | Recontextualized time-series OD curves as high-dimensional, predictive datasets |

---

## Usage

### Prerequisites

```bash
pip install -r requirements.txt
```

### Generate all figures

```bash
python generate_all.py
```

All SVG and PDF outputs are written to `output/`.

### Generate a single figure

```bash
cd figures
python figure1_horizontal_timeline.py   # → output/figure1_horizontal_timeline.{svg,pdf}
python figure2_vertical_timeline.py
python figure3_companion_table.py
python figure4_combined.py
python figure5_radial_timeline.py
```

### Customise

Edit `figures/data.py` to update any era label, timeframe, milestone text,
paradigm description, reference, or colour without touching the figure scripts.

---

## Repository Layout

```
illucidate_figures/
├── figures/
│   ├── data.py                        # Shared era data (single source of truth)
│   ├── style.py                       # Shared matplotlib publication style
│   ├── figure1_horizontal_timeline.py
│   ├── figure2_vertical_timeline.py
│   ├── figure3_companion_table.py
│   ├── figure4_combined.py
│   └── figure5_radial_timeline.py
├── icons/
│   ├── icon_microscope.svg
│   ├── icon_flask.svg
│   ├── icon_dna.svg
│   ├── icon_genome.svg
│   ├── icon_ai.svg
│   └── icon_growth_curve.svg
├── output/                            # Generated SVG + PDF files
│   ├── figure1_horizontal_timeline.svg / .pdf
│   ├── figure2_vertical_timeline.svg  / .pdf
│   ├── figure3_companion_table.svg    / .pdf
│   ├── figure4_combined.svg           / .pdf
│   └── figure5_radial_timeline.svg    / .pdf
├── generate_all.py                    # Master script — runs all figures
├── requirements.txt
└── README.md
```

---

## Design Notes

* **Colour palette** — each era has a distinct accent colour (purple → teal → green → amber → cobalt → orchid) applied consistently across all figures and icons.
* **Typography** — Lato (or DejaVu Sans as fallback) at 8–14 pt; body text renders as SVG `<text>` elements (not paths) for maximum editability.
* **SVG editability** — all vector graphics use `svg.fonttype = "none"` so text remains fully editable in Inkscape, Illustrator, or any SVG-capable editor.
* **PDF embedding** — PDFs use TrueType font embedding (`pdf.fonttype = 42`) for clean print output.
* **Resolution** — figures are saved at 300 DPI for PDF/PNG export; SVGs are resolution-independent.
