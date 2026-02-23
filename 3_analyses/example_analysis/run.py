# 3_analyses/example_analysis/run.py
# Example analysis script — use as a template for new analyses.
# Run: cd 3_analyses/example_analysis && python run.py

import sys, duckdb, json
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

DB_PATH = Path("../../2_db/project.duckdb")
if not DB_PATH.exists():
    print("⚠ Skipping: database not found at", DB_PATH)
    print("  Run 'make db' first, or delete this example folder when starting a real project.")
    sys.exit(0)

Path("figures").mkdir(exist_ok=True)
con = duckdb.connect(str(DB_PATH), read_only=True)

# ── Query ────────────────────────────────────────────────────────
query = """
SELECT 1 AS example_col, 'hello' AS example_text
"""
# Replace with your actual query, e.g.:
# query = """
#     SELECT category, COUNT(*) AS n
#     FROM my_table
#     GROUP BY category
#     ORDER BY n DESC
# """

df = con.sql(query).df()

# ── Figure (optional) ───────────────────────────────────────────
# Uncomment and adapt:
# fig, ax = plt.subplots(figsize=(8, 5))
# df.head(10).plot.barh(x="category", y="n", ax=ax)
# ax.set_xlabel("Count")
# ax.set_title("Top categories")
# fig.savefig("figures/bar_chart.pdf", bbox_inches="tight")
# plt.close()

# ── Output JSON ─────────────────────────────────────────────────
output = {
    "query": query.strip(),
    "n_results": len(df),
    "results": df.to_dict(orient="records"),
    "description": "Example analysis — replace with your description",
    "interpretation": "",  # fill after reviewing results
    "figures": [],
    # When you have figures, add them like this:
    # "figures": [{"file": "figures/bar_chart.pdf", "caption": "Top categories"}],
}

with open("results.json", "w") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)
print(f"✓ {len(df)} results → results.json")
