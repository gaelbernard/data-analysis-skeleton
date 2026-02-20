# Stage 2: Database

Transform raw data from `1_data/` into a clean, queryable DuckDB database.

## What to do

1. Edit `build_db.py` to import and transform your raw data
2. Run `python build_db.py` (or `make db` from root)
3. Review the auto-generated `schema.md` to verify the structure
4. Update `schema.md` with descriptions if needed

## Rules

- Output is always a single file: `project.duckdb`
- The DuckDB is **not committed to git** (it's in `.gitignore`) — it is rebuilt from scripts
- `schema.md` is the contract between this stage and `3_analyses/`. Keep it accurate.
- All transformations happen here: cleaning, normalizing, computing derived columns, etc.

## Files

- `build_db.py` — Master script that builds `project.duckdb`
- `schema.md` — Auto-generated database documentation (tables, columns, types)
- `project.duckdb` — The database (gitignored, rebuilt with `make db`)
