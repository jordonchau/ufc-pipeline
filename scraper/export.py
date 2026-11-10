"""Export the dbt mart tables to CSV so Tableau can read them."""
from pathlib import Path

import duckdb

DB_PATH = "data/ufc.duckdb"
EXPORT_DIR = Path("data/exports")
TABLES = ["dim_event", "dim_fighter", "fct_fights", "fct_fighter_fights"]


def main():
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(DB_PATH, read_only=True)   # read-only: export never changes the data

    for table in TABLES:
        out = EXPORT_DIR / f"{table}.csv"
        con.execute(f"COPY (SELECT * FROM {table}) TO '{out}' (HEADER, DELIMITER ',')")
        rows = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"{table}: {rows} rows -> {out}")

    con.close()


if __name__ == "__main__":
    main()
