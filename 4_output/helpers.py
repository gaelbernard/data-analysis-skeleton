# 4_output/helpers.py
# Helpers to load analysis data in Quarto documents.
#
# Each deliverable lives in a subfolder of 4_output/ (e.g. 2026-02-18-report/).
# Import from a .qmd Python chunk like this:
#
#   import sys; sys.path.insert(0, "..")
#   from helpers import load_analysis, load_figure
#
#   data = load_analysis("value_frequency")
#   fig  = load_figure("value_frequency", "bar_chart.pdf")

import json
from pathlib import Path

ANALYSES_DIR = Path(__file__).parent.parent / "3_analyses"

REQUIRED_KEYS = {"query", "n_results", "results", "description", "interpretation", "figures"}


def validate_results(data, name):
    """Check that a results.json dict conforms to the expected schema.

    Raises ValueError with a descriptive message if validation fails.
    """
    missing = REQUIRED_KEYS - set(data.keys())
    if missing:
        raise ValueError(
            f"Analysis '{name}/results.json' is missing required keys: {missing}"
        )
    if not isinstance(data["results"], list):
        raise ValueError(
            f"Analysis '{name}/results.json': 'results' must be a list, "
            f"got {type(data['results']).__name__}"
        )
    if data["n_results"] != len(data["results"]):
        raise ValueError(
            f"Analysis '{name}/results.json': 'n_results' is {data['n_results']} "
            f"but 'results' has {len(data['results'])} items"
        )
    if not isinstance(data["figures"], list):
        raise ValueError(
            f"Analysis '{name}/results.json': 'figures' must be a list, "
            f"got {type(data['figures']).__name__}"
        )
    for i, fig in enumerate(data["figures"]):
        for key in ("file", "caption"):
            if key not in fig:
                raise ValueError(
                    f"Analysis '{name}/results.json': figures[{i}] is missing '{key}'"
                )


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
    data = json.load(open(p))
    validate_results(data, name)
    return data


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
