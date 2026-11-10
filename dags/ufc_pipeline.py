"""Weekly UFC pipeline: scrape -> load -> dbt run -> dbt test.

Runs every Sunday at 10 AM Eastern, after Saturday fight night.
"""
import pendulum
from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator

PROJECT = "/opt/ufc"
PYTHON = "/opt/pipeline/bin/python"
DBT = "/opt/pipeline/bin/dbt"

with DAG(
    dag_id="ufc_pipeline",
    schedule="0 10 * * 0",                      # minute hour day month weekday (0 = Sunday)
    start_date=pendulum.datetime(2026, 11, 1, tz="America/New_York"),
    catchup=False,                              # don't backfill missed past Sundays
    default_args={"retries": 1, "retry_delay": pendulum.duration(minutes=5)},
    tags=["ufc"],
) as dag:

    scrape_events = BashOperator(
        task_id="scrape_events",
        bash_command=f"cd {PROJECT} && {PYTHON} scraper/events.py",
    )

    scrape_fights = BashOperator(
        task_id="scrape_fights",
        bash_command=f"cd {PROJECT} && {PYTHON} scraper/fights.py",
    )

    load_duckdb = BashOperator(
        task_id="load_duckdb",
        bash_command=f"cd {PROJECT} && {PYTHON} scraper/load.py",
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"cd {PROJECT}/transform && {DBT} run --profiles-dir .",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"cd {PROJECT}/transform && {DBT} test --profiles-dir .",
    )

    scrape_events >> scrape_fights >> load_duckdb >> dbt_run >> dbt_test
