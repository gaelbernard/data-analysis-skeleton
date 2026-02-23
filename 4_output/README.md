# Stage 4: Output

Produce deliverables (reports, slides, dashboards) using Quarto. Each deliverable lives in its own **dated subfolder**.

## Structure

```
4_output/
  helpers.py                        # shared Python helper
  templates/
    report.qmd                      # starter template for reports
    slides.qmd                      # starter template for slides
    dashboard.qmd                   # starter template for dashboards
    report/preamble.tex             # shared LaTeX preamble for reports
    report/titlepage.tex            # default title page (copy + customize)
    report/epfl_logo.png            # logo for title pages
    slides/preamble.tex             # shared Beamer preamble for slides
    slides/epfl_logo.png            # logo for slide title page
    dashboard/style.css             # CSS theme for dashboards
    dashboard/epfl_logo.png         # logo for dashboard navbar
  2026-02-18-short-report/          # example report deliverable
    report.qmd
    titlepage.tex
    report.pdf
  2026-03-01-final-slides/          # example slides deliverable
    slides.qmd
    slides.pdf
  2026-03-05-overview-dashboard/    # example dashboard deliverable
    dashboard.qmd
    epfl_logo.png
    dashboard.html
```

## Creating a New Deliverable

1. **Pick a name**: use `YYYY-MM-DD-short-description` (e.g. `2026-02-18-short-report`).
2. **Create the folder** and copy the template:

**Report:**
```bash
mkdir -p 4_output/2026-02-18-short-report
cp 4_output/templates/report.qmd 4_output/2026-02-18-short-report/report.qmd
cp 4_output/templates/report/titlepage.tex 4_output/2026-02-18-short-report/titlepage.tex
```

**Slides:**
```bash
mkdir -p 4_output/2026-03-01-final-slides
cp 4_output/templates/slides.qmd 4_output/2026-03-01-final-slides/slides.qmd
```

**Dashboard:**
```bash
mkdir -p 4_output/2026-03-05-overview-dashboard
cp 4_output/templates/dashboard.qmd 4_output/2026-03-05-overview-dashboard/dashboard.qmd
cp 4_output/templates/dashboard/epfl_logo.png 4_output/2026-03-05-overview-dashboard/epfl_logo.png
```

3. **Edit** the `.qmd` (and `titlepage.tex` for reports) for your project.
4. **Render**:

```bash
make render d=2026-02-18-short-report
# or render all deliverables:
make outputs
```

## The Golden Rule

**Never write a number directly in a Quarto document.** Every number, count, percentage, or statistic must be loaded from a `results.json` in `3_analyses/`. If the data you need doesn't exist, go back and create a new analysis first.

## Loading Data

In the first Python chunk of your `.qmd`:

```python
import sys; sys.path.insert(0, "..")
from helpers import load_analysis, load_figure, load_value

data = load_analysis("value_frequency")
# data["results"]        -> list of dicts
# data["n_results"]      -> int
# data["interpretation"] -> string

fig_path = load_figure("value_frequency", "bar_chart.pdf")

# For dashboards: extract a single scalar for value boxes
total = load_value("value_frequency", "count", agg="sum")
```

## Report Conventions

The `templates/report.qmd` template follows a standard structure:

1. **Disclaimer** (orange box): Flag data limitations, AI usage, methodology choices, and scope.
2. **Executive Summary** (unnumbered): Overview with key findings in a highlight box.
3. **Body** (numbered sections): Introduction, Methodology, Results, Discussion, Conclusion.
4. **Appendices** (unnumbered): Detailed tables referenced from the main text.

### LaTeX Environments

The preamble (`templates/report/preamble.tex`) provides three custom environments:

- `disclaimerbox`: Orange box for disclaimers and caveats.
- `reportbox`: Neutral highlight box (gray background, dark left bar) for key findings and takeaways.
- `docquote`: Left-bordered block for quoting source documents with attribution.

### Tables and Figures

- Tables: booktabs style, always with `\caption`, `\label`, and `[H]` placement.
- Figures: generated in `3_analyses/`, loaded via `load_figure()`. Always `[H]` with caption.
- Large tables go in appendices, referenced from the main text.

## Slides Conventions

The `templates/slides.qmd` template follows a standard structure:

1. **Disclaimer slide**: Orange disclaimer box near the beginning for data caveats and scope.
2. **One idea per slide**: Keep text minimal, let figures and data speak.
3. **Tables**: Booktabs style, max 5-6 rows to fit on a slide.
4. **Figures**: Generated in `3_analyses/`, referenced via `load_figure()`.

The Beamer preamble (`templates/slides/preamble.tex`) provides a `disclaimerbox` environment matching the report style.

## Dashboard Conventions

The `templates/dashboard.qmd` template produces an interactive HTML dashboard:

1. **Pages** (`#` headings): Each creates a navigation tab. Use "Overview" and "About".
2. **Value boxes**: Use `load_value()` to extract scalars for KPI displays.
3. **Interactive plots**: Prefer plotly or altair over static matplotlib.
4. **About page**: Include a `.disclaimer-box` div for data caveats.
5. **Logo**: Copy `templates/dashboard/epfl_logo.png` into each dashboard subfolder.

The CSS theme (`templates/dashboard/style.css`) provides a modern colorful design with indigo navbar and clean card layout.
