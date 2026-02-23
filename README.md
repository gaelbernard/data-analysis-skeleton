# Data Analysis Skeleton

A structured pipeline for data analysis projects. Data flows forward through five stages:

```
0_plan  →  1_data  →  2_db  →  3_analyses  →  4_output
```

## Getting Started

```bash
pip install -r requirements.txt
cp .env.example .env       # fill in your API keys
```

## What to Do at Each Stage

### 0. Plan (`0_plan/`)

Define your project before writing any code. Open a conversation with the AI, brainstorm your idea, then say "let's finalize the plan" to fill in `plan.md`. Done when every section has real content.

→ See [`0_plan/README.md`](0_plan/README.md)

### 1. Collect Data (`1_data/`)

Gather the raw data listed in your plan. Drop files here and document each one in `sources.yaml`. Never modify raw files after collection. Done when every planned source has a file and a `sources.yaml` entry.

→ See [`1_data/README.md`](1_data/README.md)

### 2. Build the Database (`2_db/`)

Transform raw data into a clean DuckDB. Edit `build_db.py`, then run `make db`. The script reads from `1_data/`, applies all transformations, and produces `project.duckdb` + `schema.md`. Done when the DB builds cleanly and the schema looks right.

→ See [`2_db/README.md`](2_db/README.md)

### 3. Analyze (`3_analyses/`)

Answer your research questions. Each analysis lives in its own subfolder with a `run.py` that queries the DB and writes a `results.json`. The AI will propose a first batch based on your plan. Run all with `make analyses`. Done when every question from the plan has a valid `results.json`.

→ See [`3_analyses/README.md`](3_analyses/README.md)

### 4. Produce Output (`4_output/`)

Write the final report, slides, or dashboard in Quarto. All numbers come from `3_analyses/` via `helpers.py` (never hardcode). Render with `make render d=<folder>` or `make outputs`.

→ See [`4_output/README.md`](4_output/README.md)

## Make Commands

```bash
make status                     # Show pipeline status and validation
make db                         # Build the DuckDB from 1_data/
make analyses                   # Run all analysis scripts
make render d=<folder>          # Render a specific deliverable in 4_output/
make outputs                    # Render all deliverables
make all                        # Full pipeline: db → analyses → outputs
make clean                      # Remove generated files
make skeleton-sync msg="..."    # Commit + push skeleton improvements
```

## Prerequisites

- Python 3.10+
- [Quarto](https://quarto.org/docs/get-started/) (for rendering reports/slides)
- LuaLaTeX (e.g., TeX Live or MacTeX)

## Skeleton Management

This project is based on a reusable template. To backport improvements or pull updates, see [`SKELETON.md`](SKELETON.md).
