# Stage 4: Output

Produce the final deliverable (report, slides) using Quarto.

## What to do

1. Tell the LLM you're ready to produce the deliverable (report or slides -- pick one to start).
2. The LLM will review available analyses and propose a structure.
3. It will write the `.qmd`, pulling all data from `3_analyses/` via `helpers.py`.
4. If simple data is missing, the LLM will create new analyses in `3_analyses/` autonomously.
5. Customize `templates/report/titlepage.tex` with your project details.
6. Render with `make report` or `make slides`.

## The Golden Rule

**Never write a number directly in a Quarto document.** Every number, count, percentage, or statistic must be loaded from a `results.json` in `3_analyses/`. If the data you need doesn't exist, go back and create a new analysis first.

## Report Conventions

The `report.qmd` template follows a standard structure:

1. **Disclaimer** (orange box): Flag data limitations, AI usage, methodology choices, and scope.
2. **Executive Summary** (unnumbered): Overview with key findings in a highlight box.
3. **Body** (numbered sections): Introduction, Methodology, Results, Discussion, Conclusion.
4. **Appendices** (unnumbered): Detailed tables referenced from the main text.

### LaTeX Environments

The preamble (`templates/report/preamble.tex`) provides three custom environments:

- `disclaimerbox` -- Orange box for disclaimers and caveats.
- `reportbox` -- Neutral highlight box (gray background, dark left bar) for key findings and takeaways.
- `docquote` -- Left-bordered block for quoting source documents with attribution.

### Tables and Figures

- Tables: booktabs style, always with `\caption`, `\label`, and `[H]` placement.
- Figures: generated in `3_analyses/`, loaded via `load_figure()`. Always `[H]` with caption.
- Large tables go in appendices, referenced from the main text.

## Loading Data

In a Python chunk inside your `.qmd`:

```python
from helpers import load_analysis, load_figure

data = load_analysis("value_frequency")
# data["results"]        -> list of dicts
# data["n_results"]      -> int
# data["interpretation"] -> string

fig_path = load_figure("value_frequency", "bar_chart.pdf")
```

## Rendering

```bash
make report     # or: cd 4_output && quarto render report.qmd
make slides     # or: cd 4_output && quarto render slides.qmd
```

## Files

- `helpers.py` -- Python helpers to load analysis JSONs and figures
- `report.qmd` -- Report template (Quarto + LuaLaTeX -> PDF)
- `slides.qmd` -- Slides template (Quarto Beamer -> PDF)
- `templates/report/preamble.tex` -- LaTeX preamble with custom environments and styles
- `templates/report/titlepage.tex` -- Custom title page (edit per project)
- `templates/report/epfl_logo.png` -- Logo for the title page
- `templates/slides/` -- Beamer theme customizations
