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
#   make skeleton-sync msg="..."  Commit + push skeleton improvements
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

# Commit skeleton changes and push to the skeleton remote automatically.
# Usage: make skeleton-sync msg="improve Makefile with clean target"
# The changed files must be staged (git add) before running this.
skeleton-sync:
	@if [ -z "$(msg)" ]; then \
		echo "✗ Usage: make skeleton-sync msg=\"description of the change\""; \
		exit 1; \
	fi
	git commit -m "[skeleton] $(msg)"
	@if git remote get-url skeleton >/dev/null 2>&1; then \
		HASH=$$(git rev-parse HEAD) && \
		git fetch skeleton && \
		git checkout -b _skeleton_backport skeleton/main && \
		if git cherry-pick $$HASH; then \
			git push skeleton _skeleton_backport:main && \
			echo "✓ Pushed to skeleton remote"; \
		else \
			echo "✗ Cherry-pick conflict. Resolve manually:"; \
			echo "  git cherry-pick --abort  (to cancel)"; \
			echo "  git cherry-pick --continue  (after resolving)"; \
			git cherry-pick --abort; \
		fi; \
		git checkout - && \
		git branch -D _skeleton_backport 2>/dev/null || true; \
	else \
		echo "⚠ No 'skeleton' remote found. Committed locally with [skeleton] prefix."; \
		echo "  To set up: git remote add skeleton <skeleton-repo-url>"; \
	fi

.PHONY: db analyses report slides all clean skeleton-sync
