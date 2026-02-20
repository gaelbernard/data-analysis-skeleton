# Stage 3: Analyses

Query the DuckDB and produce structured JSON outputs (+ optional figures).

## How to use

1. Check `0_plan/plan.md` -- the "Analyses" section lists the questions to answer.
2. Read `2_db/schema.md` to understand available tables and columns.
3. On first entry, the LLM will propose a batch of analyses based on the plan and schema. Review, adjust, and confirm.
4. Run `make analyses` (from root) to execute all, or `cd 3_analyses/my_analysis && python run.py` for one.
5. Refine iteratively: adjust queries, add figures, update interpretations.

## Structure

```
3_analyses/
  value_frequency/
    run.py              # Script
    results.json        # Output (JSON)
    figures/            # Optional
      bar_chart.pdf
  another_analysis/
    run.py
    results.json
```

## JSON Schema

Every `results.json` must have this structure:

```json
{
  "query": "SELECT ...",
  "n_results": 10,
  "results": [{"col": "val", ...}, ...],
  "description": "What this analysis does (English)",
  "interpretation": "What the results mean (English)",
  "figures": [
    {"file": "figures/chart.pdf", "caption": "What the figure shows"}
  ]
}
```

## Rules

- Connect with `read_only=True`: never modify the DB from here
- Run scripts from their subfolder: `cd 3_analyses/my_analysis && python run.py`
- Figures must use the same data as the JSON (or a subset, never more)
- If the DB schema changes, re-run affected analyses (`make analyses`)
- Never delete old analyses -- prefix with `_deprecated_` if superseded

## When is this stage done?

When every analysis question from the plan has a subfolder with a valid `results.json` and interpretations have been reviewed. Then move to `4_output/`.

## Example

See `example_analysis/` for a working template.
