# Stage 3: Analyses

Query the DuckDB and produce structured JSON outputs (+ optional figures).

## What to do

1. Create a subfolder for each analysis (use a descriptive `snake_case` name)
2. Write a `run.py` that queries the DB and outputs `results.json`
3. Optionally generate figures in a `figures/` subfolder
4. Run `make analyses` (from root) to execute all analyses, or `cd 3_analyses/my_analysis && python run.py` for a single one

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
- Never delete old analyses — prefix with `_deprecated_` if superseded

## Example

See `example_analysis/` for a working template.
