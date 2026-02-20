# Agent Instructions

You are assisting with a data analysis project that follows a structured pipeline. Read this document carefully before doing any work.

## Pipeline Overview

The project is organized into 5 stages. Data flows forward only — never skip a stage or create backward dependencies.

```
0_plan  →  1_data  →  2_db  →  3_analyses  →  4_output
```

| Stage | Reads from | Produces | Format |
|-------|-----------|----------|--------|
| `0_plan/` | (nothing) | plan.md, decisions.md | Markdown |
| `1_data/` | External sources | Raw data files + sources.yaml | CSV, JSON, XLSX, etc. |
| `2_db/` | `1_data/*` | `project.duckdb` + `schema.md` | DuckDB + Markdown |
| `3_analyses/` | `2_db/project.duckdb` | `results.json` + optional figures per subfolder | JSON + PDF/PNG |
| `4_output/` | `3_analyses/*/results.json` | Report, slides | Quarto → PDF |

## General Rules

- **Language**: Python. Use Pandas unless instructed otherwise.
- **Coding style**: Write concise, flat scripts. No `if __name__ == "__main__"`. Minimize functions — use them only when they genuinely reduce repetition. Top-level procedural code is preferred.
- **API keys**: Never hardcode API keys. Use a `.env` file with `python-dotenv`. See `.env.example` for the template.
- **Dependencies**: All Python dependencies go in `requirements.txt` at the root.
- **Skeleton improvements**: When you modify a generic file that could benefit future projects (agents.md, Makefile, helpers.py, templates, READMEs), prefix the commit message with `[skeleton]`. Example: `git commit -m "[skeleton] improve JSON schema documentation"`.
- **Stage gates**: Before starting work in any stage, verify that prerequisite stages are complete. If `plan.md` still has placeholders, don't start collecting data. If `sources.yaml` is missing entries for files in `1_data/`, don't build the DB or run analyses. If documentation or provenance is unclear, **stop and ask the user to fill the gaps before proceeding**. Never skip a stage just because the user is eager to move forward.

---

## Stage 0: Plan (`0_plan/`)

**Goal**: Define the project before writing any code.

**How to detect you're in Stage 0**: Check `0_plan/plan.md`. If it still contains placeholder text (italicized prompts like _What question are we answering?_), the plan is incomplete. Also check whether `2_db/project.duckdb` exists — if not, the project hasn't moved past planning.

### Two phases

#### Phase 1: Brainstorming (free-form)

The user may open multiple conversations to explore ideas. During this phase:

- Engage naturally. Help the user think through their project idea.
- Ask clarifying questions, suggest approaches, challenge assumptions.
- **Don't pressure to fill in `plan.md`** — the user is still thinking.
- **Don't try to record everything** — conversations are ephemeral by design. The user will start fresh sessions and that's fine.

#### Phase 2: Consolidation (structured)

When the user signals they're ready — or when you sense the idea is mature enough — switch to consolidation:

1. **Summarize** your understanding of the project in a few sentences.
2. **Ask for confirmation**: "Does this overall direction look right?"
3. **Once confirmed**, read `0_plan/plan.md` and systematically identify which sections are still empty or placeholder.
4. **Ask targeted questions** for each gap — don't ask everything at once, go section by section.
5. **Fill in `plan.md`** with the agreed answers.

The user can trigger consolidation explicitly (e.g., "let's finalize the plan") or you can suggest it when the conversation has covered enough ground.

### Files

- `plan.md` — The project plan. Starts as a template; complete it during Phase 2.
- `decisions.md` — Decision log. Update throughout the project (not just Stage 0).

**When to update the plan**: If later stages reveal that the original plan doesn't work (wrong data, unexpected results), update `plan.md` and log the decision in `decisions.md`.

---

## Stage 1: Data Collection (`1_data/`)

**Goal**: Gather all raw data needed for the project.

**How to detect you're in Stage 1**: `0_plan/plan.md` is complete (no placeholder text), but `1_data/` has no actual data files yet — or has some but not all files listed in the plan's "Input Data" section.

### What the agent should do

1. **Read the plan**: Start by reading `0_plan/plan.md`, especially the "Input Data" section, to know what data is needed.
2. **Help collect**: Depending on the situation:
   - If the user drops files into `1_data/` manually, help document them in `sources.yaml`.
   - If data comes from an API, write a collection script in `1_data/` (e.g., `fetch_*.py`).
   - If the user needs help finding data, suggest sources based on the plan.
3. **Document everything**: After each file is added, update `sources.yaml` with its provenance.
4. **Check completeness**: Cross-reference the plan's "Input Data" table with what's actually in `1_data/`. Flag anything missing.

### Rules

- Every data file must be documented in `sources.yaml` with: filename, origin, URL (if applicable), date accessed, description, format, and `confidential` flag.
- **Confidentiality**: All data is public by default (`confidential: false`). If a file is confidential (`confidential: true`), it must be added to `.gitignore` so it is never committed. The `sources.yaml` entry itself is still committed — only the data file is excluded.
- Raw data is committed to git (unless too large or confidential — in either case, document how to obtain it and add a download script in `1_data/`).
- Never modify raw data files after collection. All transformations happen in `2_db/`.
- If data comes from an API or database, write a collection script in `1_data/` and document it in `sources.yaml`.

### When is Stage 1 done?

Every data source listed in the plan has a corresponding file in `1_data/` and an entry in `sources.yaml`. This is enforced — the agent will refuse to proceed to later stages if documentation is incomplete. Then move to `2_db/`.

---

## Stage 2: Database (`2_db/`)

**Goal**: Transform raw data into a clean, queryable DuckDB database.

Rules:
- The output is always a single file: `project.duckdb`.
- The build script is `build_db.py`. It reads from `1_data/`, applies all transformations, and writes the DuckDB.
- Transformations include: importing raw files, cleaning text, normalizing values, computing derived columns (embeddings, categories, etc.), creating lookup tables.
- After building, auto-generate `schema.md` documenting all tables, columns, and types.
- The DuckDB is not committed to git (it's in `.gitignore`). It is rebuilt with `make db` or `python 2_db/build_db.py`.

**Important**: `schema.md` is the contract between `2_db/` and `3_analyses/`. Always keep it up to date. When the LLM writes SQL queries in `3_analyses/`, it should reference `schema.md` to know the exact table and column names.

---

## Stage 3: Analyses (`3_analyses/`)

**Goal**: Answer analytical questions by querying the DuckDB and producing structured JSON outputs.

### Pre-flight check

Before writing or running any analysis, verify:

1. **Plan exists**: `0_plan/plan.md` is filled in (no placeholder text).
2. **Data is documented**: Every data file in `1_data/` has a corresponding entry in `sources.yaml` with origin, date, and description. If any file is undocumented or provenance is unclear, **stop and ask the user to complete `sources.yaml` before proceeding**.
3. **DB is built**: `2_db/project.duckdb` exists and `2_db/schema.md` is up to date.

Do not skip these checks. Incomplete provenance upstream makes analysis results unreliable and unreproducible.

### Structure

Each analysis lives in its own subfolder:

```
3_analyses/
  value_frequency/
    run.py              # Script: queries DB, writes results.json + optional figures
    results.json        # Output: structured JSON (see schema below)
    figures/            # Optional: figures generated by run.py
      bar_chart.pdf
  schein_levels/
    run.py
    results.json
  ...
```

### The JSON Contract

Every `results.json` must follow this schema:

```json
{
  "query": "SELECT ... FROM ...",
  "n_results": 38,
  "results": [
    {"col1": "value1", "col2": 123},
    {"col1": "value2", "col2": 456}
  ],
  "description": "Short sentence: what this analysis does",
  "interpretation": "Short sentence: what the results mean",
  "figures": [
    {
      "file": "figures/bar_chart.pdf",
      "caption": "What this figure shows"
    }
  ]
}
```

Fields:
- `query`: The exact SQL query used. Must be valid against the current `schema.md`.
- `n_results`: Number of rows in `results`.
- `results`: Array of objects — the raw query output in JSON format.
- `description`: One sentence explaining what we tried to do (in English).
- `interpretation`: One sentence interpreting the results (in English). Can be left empty initially and filled after reviewing.
- `figures`: Array of figure references (empty `[]` if no figures). Each entry has `file` (relative path) and `caption`.

### Rules for Analysis Scripts (`run.py`)

- Always connect to the DuckDB with `read_only=True`: `con = duckdb.connect("../../2_db/project.duckdb", read_only=True)`
- The script should be runnable from its own subfolder: `cd 3_analyses/my_analysis && python run.py`
- Output `results.json` in the same subfolder.
- If the DB schema changes, the query may break or return different results. In that case, update the query and re-run the script.
- Keep scripts concise and flat. No `if __name__ == "__main__"`.

### Rules for Figures

- Figures go in a `figures/` subfolder within the analysis folder.
- A figure must use the same data as the JSON results (or a subset). Never fetch additional data for a figure that isn't in the JSON.
- Every figure must be referenced in the `figures` array of `results.json`.
- Prefer PDF for vector graphics, PNG for raster.

### When to Create a New Analysis vs. Update an Existing One

- **New subfolder**: when answering a new question.
- **Update existing**: when refining the same question (adding a filter, changing a grouping).
- **Never delete**: if an analysis is superseded, rename the folder with a `_deprecated_` prefix.

---

## Stage 4: Output (`4_output/`)

**Goal**: Produce the final deliverable (report, slides, etc.) using Quarto.

### The Golden Rule

**Never write a number directly in a Quarto document.** Every number, count, percentage, or statistic must be loaded from a `results.json` in `3_analyses/`. If the data you need doesn't exist as a JSON, go back to `3_analyses/` and create a new analysis first.

### Loading Data

Use `helpers.py` to load analysis data in Quarto Python chunks:

```python
from helpers import load_analysis, load_figure

data = load_analysis("value_frequency")
# data["results"] → list of dicts
# data["n_results"] → int
# data["interpretation"] → string

fig_path = load_figure("value_frequency", "bar_chart.pdf")
```

### Figures in Reports

Figures are generated in `3_analyses/` (not in `4_output/`). The report references them by path using `load_figure()`. This ensures figures and data stay in sync.

### Templates

- `templates/report/` — LaTeX preamble, title page, styles for reports.
- `templates/slides/` — Beamer theme files for slides.

Customize these per project. When you create a reusable template improvement, commit with `[skeleton]` prefix.

### Rendering

```bash
cd 4_output && quarto render report.qmd
cd 4_output && quarto render slides.qmd
```

Or use `make report` / `make slides` from the project root.

---

## Orchestration (Makefile)

The `Makefile` at the root provides shortcuts:

```bash
make db          # Rebuild DuckDB from 1_data/
make analyses    # Run all run.py scripts in 3_analyses/
make report      # Render report with Quarto
make slides      # Render slides with Quarto
make all         # Run the full pipeline: db → analyses → report
```

---

## Troubleshooting Checklist

If something breaks, check in this order:

1. **Report shows wrong numbers?** → Re-run the analysis (`make analyses`), then re-render (`make report`).
2. **Analysis query fails?** → Check `2_db/schema.md` — did the DB schema change? Update the query in `run.py`.
3. **DB build fails?** → Check that raw data in `1_data/` hasn't changed format. Update `build_db.py`.
4. **Missing data for the report?** → Create a new analysis subfolder in `3_analyses/`. Never hardcode.
5. **API key error?** → Check `.env` file exists and has the right keys. See `.env.example`.
