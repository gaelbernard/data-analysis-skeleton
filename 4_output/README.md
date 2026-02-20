# Stage 4: Output

Produce the final deliverable (report, slides) using Quarto.

## What to do

1. Edit `report.qmd` and/or `slides.qmd`
2. Use `helpers.py` to load data from `3_analyses/` — never hardcode numbers
3. Customize templates in `templates/report/` or `templates/slides/`
4. Render with `make report` or `make slides` (from root)

## The Golden Rule

**Never write a number directly in a Quarto document.** Every number, count, percentage, or statistic must be loaded from a `results.json` in `3_analyses/`. If the data you need doesn't exist, go back and create a new analysis first.

## Loading Data

In a Python chunk inside your `.qmd`:

```python
from helpers import load_analysis, load_figure

data = load_analysis("value_frequency")
# data["results"]        → list of dicts
# data["n_results"]      → int
# data["interpretation"] → string

fig_path = load_figure("value_frequency", "bar_chart.pdf")
```

## Rendering

```bash
make report     # or: cd 4_output && quarto render report.qmd
make slides     # or: cd 4_output && quarto render slides.qmd
```

## Files

- `helpers.py` — Python helpers to load analysis JSONs and figures
- `report.qmd` — Report template (Quarto → PDF)
- `slides.qmd` — Slides template (Quarto Beamer → PDF)
- `templates/report/` — LaTeX preamble, title page, styles
- `templates/slides/` — Beamer theme customizations
