import duckdb

DB_PATH = "data/ufc.duckdb"

TABLES = {
    "events": "data/raw/events.csv",
    "fights": "data/raw/fights.csv",
}


def main():
    con = duckdb.connect(DB_PATH)                  # open (or create) the database file
    con.execute("CREATE SCHEMA IF NOT EXISTS raw") # a "raw" folder for untouched data

    for table, csv_path in TABLES.items():
        con.execute(f"""
            CREATE OR REPLACE TABLE raw.{table} AS
            SELECT * FROM read_csv_auto('{csv_path}')
        """)                                       # load the CSV; DuckDB guesses column types
        count = con.execute(f"SELECT COUNT(*) FROM raw.{table}").fetchone()[0]
        print(f"raw.{table}: {count} rows")

    con.close()


if __name__ == "__main__":
    main()