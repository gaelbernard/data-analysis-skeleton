# ============================================================================
# Makefile — Data Analysis Pipeline
# ============================================================================
# Usage:
#   make db          Build the DuckDB database from raw data in 1_data/
#   make analyses    Run all analysis scripts in 3_analyses/
#   make report      Render the Quarto report (PDF)
#   make slides      Render the Quarto slides (PDF)
#   make all         Run the full pipeline: db → analyses → report
#   make clean       Remove generated files (DuckDB, JSONs, figures, PDFs)
# ============================================================================

# Build the DuckDB database
db:
	python 2_db/build_db.py

# Run every run.py found in 3_analyses/ subfolders
analyses:
	@for dir in 3_analyses/*/; do \
		if [ -f "$$dir/run.py" ]; then \
			echo "▶ Running $$dir"; \
			(cd "$$dir" && python run.py); \
		fi; \
	done

# Render report
report:
	cd 4_output && quarto render report.qmd

# Render slides
slides:
	cd 4_output && quarto render slides.qmd

# Full pipeline
all: db analyses report

# Clean generated files
clean:
	rm -f 2_db/project.duckdb 2_db/*.wal
	find 3_analyses -name "results.json" -delete
	find 3_analyses -type d -name "figures" -exec rm -rf {} + 2>/dev/null || true
	rm -f 4_output/*.pdf 4_output/*.tex 4_output/*.log
	rm -rf 4_output/*_files/

.PHONY: db analyses report slides all clean
