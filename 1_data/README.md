# Stage 1: Data Collection

Gather all raw data needed for the project. This folder holds every raw data file and a YAML manifest documenting their provenance.

## How to use

1. Check `0_plan/plan.md` → the "Input Data" section lists what you need to collect.
2. Add raw data files to this folder (CSV, JSON, XLSX, PDF, etc.).
3. Document each file in `sources.yaml` — the LLM can help with this.
4. For API or database sources, write a collection script here (e.g., `fetch_survey.py`).

## Rules

- **Never modify raw data** after collection. All transformations happen in `2_db/`.
- **Always document** the source in `sources.yaml` — even for a simple copy-paste.
- Raw data is committed to git unless too large. If too large, document how to obtain it and add a download script.
- **Confidentiality**: All data is public by default. If a file is confidential, mark `confidential: true` in `sources.yaml` and add the file to `.gitignore`. The `sources.yaml` entry is still committed — only the data file is excluded.

## When is this stage done?

When every data source from the plan has a file here and an entry in `sources.yaml`. Then move to `2_db/`.

## Files

- `sources.yaml` — Machine-readable provenance for every data file
