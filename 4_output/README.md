# Stage 4: Output

Produce deliverables (reports, slides) using Quarto. Each deliverable lives in its own **dated subfolder**.

## Structure

```
4_output/
  helpers.py                        # shared Python helper
  templates/
    report.qmd                      # starter template for reports
    slides.qmd                      # starter template for slides
    report/preamble.tex             # shared LaTeX preamble for reports
    report/titlepage.tex            # default title page (copy + customize)
    report/epfl_logo.png            # logo for title pages
    slides/preamble.tex             # shared Beamer preamble for slides
    slides/epfl_logo.png            # logo for slide title page
  2026-02-18-short-report/          # example deliverable
    report.qmd
    titlepage.tex
    report.pdf
```

## Creating a New Deliverable

1. **Pick a name**: use `YYYY-MM-DD-short-description` (e.g. `2026-02-18-short-report`).
2. **Create the folder** and copy the template:

```bash
mkdir -p 4_output/2026-02-18-short-report
cp 4_output/templates/report.qmd 4_output/2026-02-18-short-report/report.qmd
# For reports, also copy the title page:
cp 4_output/templates/report/titlepage.tex 4_output/2026-02-18-short-report/titlepage.tex
```

3. **Edit** the `.qmd` and `titlepage.tex` for your project.
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
from helpers import load_analysis, load_figure

data = load_analysis("value_frequency")
# data["results"]        -> list of dicts
# data["n_results"]      -> int
# data["interpretation"] -> string

fig_path = load_figure("value_frequency", "bar_chart.pdf")
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
