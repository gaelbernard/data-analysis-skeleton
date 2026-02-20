# Stage 1: Data Collection

Gather all raw data needed for the project. Document every data source.

## What to do

1. Collect raw data files (CSV, JSON, XLSX, PDF, etc.) into this folder
2. Document each file in `sources.yaml` (origin, date, description)
3. If data comes from an API or database, write a collection script here

## Rules

- **Never modify raw data** after collection. All transformations happen in `2_db/`.
- **Always document** the source in `sources.yaml` — even for a simple copy-paste.
- Raw data is committed to git unless too large. If too large, document how to obtain it.

## Files

- `sources.yaml` — Machine-readable provenance for every data file
