# Data Analysis Skeleton

A reusable project structure for data analysis projects. Each stage has its own folder, and data flows forward through a clear pipeline:

```
0_plan  →  1_data  →  2_db  →  3_analyses  →  4_output
(plan)    (collect)  (transform) (analyze)    (report)
```

## Stages

| Folder | Input | Output | Purpose |
|--------|-------|--------|---------|
| `0_plan/` | Your brain + LLM | `plan.md`, `decisions.md` | Define objectives, data sources, methods, output format |
| `1_data/` | External sources | Raw files + `sources.yaml` | Collect and document all raw data |
| `2_db/` | `1_data/*` | `project.duckdb` + `schema.md` | Clean, transform, normalize → single DuckDB |
| `3_analyses/` | `2_db/project.duckdb` | JSON + optional figures per subfolder | Run SQL queries, interpret results, generate figures |
| `4_output/` | `3_analyses/*/results.json` | PDF report, slides, etc. | Write the final deliverable with Quarto |

## Prerequisites

- **Python 3.10+**
- **Quarto** ([quarto.org](https://quarto.org/docs/get-started/)): needed for rendering reports and slides in `4_output/`.
- **LuaLaTeX**: the report template uses `lualatex` as the PDF engine. Install a TeX distribution (e.g., TeX Live or MacTeX).
- **Helvetica Neue** font: used by the report preamble. Pre-installed on macOS; on Linux, install `texlive-fonts-extra` or substitute in `preamble.tex`.

## Quick Start

```bash
pip install -r requirements.txt
cp .env.example .env       # fill in your API keys
```

Then follow the pipeline: plan → collect data → build DB → run analyses → render output.

```bash
make db              # Build the DuckDB from 1_data/
make analyses        # Run all analysis scripts in 3_analyses/
make report          # Render the Quarto report
make slides          # Render the Quarto slides
make all             # Run everything in order
make skeleton-sync msg="..."  # Commit + push skeleton improvements
```

## Key Rules

1. **Data flows forward only**: `1_data → 2_db → 3_analyses → 4_output`. Never skip a stage.
2. **Never hardcode numbers in reports**: load everything from JSON files in `3_analyses/`.
3. **DuckDB is read-only in `3_analyses/`**: the DB is only modified in `2_db/`.
4. **One subfolder per analysis** in `3_analyses/`: each has a `run.py` + `results.json` + optional `figures/`.
5. **Figures use the same data as their JSON** (or a subset, never more).
6. **Document data sources** in `1_data/sources.yaml`.
7. **API keys** go in `.env` (never committed). See `.env.example` for the template.

## How to Use This Skeleton

### Starting a New Project

1. Clone the skeleton:
```bash
git clone https://github.com/YOUR_USERNAME/data-analysis-skeleton.git my-new-project
cd my-new-project
```

2. Rename the skeleton remote (keeps the link for future backporting):
```bash
git remote rename origin skeleton
```

3. Create a new GitHub repo for your project (e.g., `my-new-project`), then:
```bash
git remote add origin https://github.com/YOUR_USERNAME/my-new-project.git
git push -u origin main
```

Now your project has two remotes:
- `origin` → your project's repo (where all your work goes)
- `skeleton` → the skeleton template repo (for backporting improvements)

4. Set up the environment:
```bash
pip install -r requirements.txt
cp .env.example .env   # edit with your actual API keys
```

5. Start with `0_plan/plan.md` — fill in your objectives, data sources, and plan.

### During a Project: Improving the Skeleton

Sometimes you'll improve something generic (a better `agents.md` rule, a `Makefile` tweak, a better template). When you do, stage the files and use `make skeleton-sync`:

```bash
git add agents.md
make skeleton-sync msg="add rule about figure naming convention"
```

This will:
1. Commit the staged files to your project with a `[skeleton]` prefix.
2. If the `skeleton` remote is configured, automatically cherry-pick the commit and push it there.
3. If no `skeleton` remote exists, it commits locally (you can backport later).

The AI agent follows this same workflow automatically when it modifies skeleton files.

### Pulling Skeleton Updates into a Running Project

If you improved the skeleton (from another project) and want to pull those updates:

```bash
git fetch skeleton
git merge skeleton/main --allow-unrelated-histories
```

Resolve any conflicts if needed, then continue working.

## For the AI Agent

See `agents.md` for the full pipeline philosophy and rules. The LLM agent should read it before starting any work.
