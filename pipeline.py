"""Run the full UFC pipeline: scrape -> load -> transform -> test.

Usage (from the ufc-pipeline folder, with the venv active):
    python pipeline.py
"""
import subprocess
import sys
import time
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
DBT = str(Path(sys.executable).parent / "dbt")   # the dbt installed in this venv

STEPS = [
    ("Scrape events", [sys.executable, "scraper/events.py"], PROJECT_DIR),
    ("Scrape fights", [sys.executable, "scraper/fights.py"], PROJECT_DIR),
    ("Load into DuckDB", [sys.executable, "scraper/load.py"], PROJECT_DIR),
    ("dbt run", [DBT, "run"], PROJECT_DIR / "transform"),
    ("dbt test", [DBT, "test"], PROJECT_DIR / "transform"),
]


def main():
    pipeline_start = time.time()

    for i, (name, command, folder) in enumerate(STEPS, start=1):
        print(f"\n=== [{i}/{len(STEPS)}] {name} ===")
        step_start = time.time()
        result = subprocess.run(command, cwd=folder)

        if result.returncode != 0:
            print(f"\nPipeline FAILED at step: {name}")
            sys.exit(1)

        print(f"--- {name} done in {time.time() - step_start:.0f}s")

    print(f"\nPipeline finished in {time.time() - pipeline_start:.0f}s")


if __name__ == "__main__":
    main()
