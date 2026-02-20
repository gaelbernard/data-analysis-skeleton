# 4_output/helpers.py
# Helpers to load analysis data in Quarto documents.
#
# Usage in a Quarto Python chunk:
#   from helpers import load_analysis, load_figure
#   data = load_analysis("value_frequency")
#   fig  = load_figure("value_frequency", "bar_chart.pdf")

import json
from pathlib import Path

ANALYSES_DIR = Path(__file__).parent.parent / "3_analyses"


def load_analysis(name):
    """Load results.json from a named analysis subfolder.

    Args:
        name: subfolder name in 3_analyses/ (e.g., "value_frequency")

    Returns:
        dict with keys: query, n_results, results, description, interpretation, figures
    """
    p = ANALYSES_DIR / name / "results.json"
    if not p.exists():
        raise FileNotFoundError(
            f"Analysis '{name}' not found at {p}. "
            f"Run: cd 3_analyses/{name} && python run.py"
        )
    return json.load(open(p))


def load_figure(name, fig_name):
    """Return the path to a figure from a named analysis.

    Args:
        name: subfolder name in 3_analyses/ (e.g., "value_frequency")
        fig_name: filename of the figure (e.g., "bar_chart.pdf")

    Returns:
        str path to the figure file
    """
    p = ANALYSES_DIR / name / "figures" / fig_name
    if not p.exists():
        raise FileNotFoundError(
            f"Figure '{fig_name}' not found in analysis '{name}' at {p}. "
            f"Run: cd 3_analyses/{name} && python run.py"
        )
    return str(p)
