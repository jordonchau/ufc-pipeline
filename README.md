# UFC Fight Analytics Pipeline

An automated ELT pipeline that collects every UFC fight since 1994, models it into a tested star schema, and powers a public Tableau dashboard. It refreshes itself every Sunday after fight night.

**[View the live dashboard on Tableau Public]([TABLEAU_LINK_HERE](https://public.tableau.com/views/UFCFightAnalytics_17943355153240/Dashboard1?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link))**

| | |
|---|---|
| Events | 796 (UFC 2, March 1994 → November 2026) |
| Fights | 8,988 |
| Fighters | 2,779 |
| Data tests | 15, run on every refresh |
| Refresh | Weekly (Sundays 10 AM ET) via Airflow |

## Architecture

```
ufcstats.com
     │  Python + Playwright scraper (HTML cached locally)
     ▼
data/raw/*.csv          ← raw layer
     │  load.py
     ▼
DuckDB  raw.events, raw.fights
     │  dbt
     ▼
staging   stg_events, stg_fights          (cleaned, typed, standardized)
     │
     ▼
marts     dim_event, dim_fighter,         (star schema)
          fct_fights, fct_fighter_fights
     │  export.py
     ▼
Tableau Public dashboard

All steps orchestrated by Apache Airflow, running in Docker.
```

## Tech stack

- **Ingestion:** Python, Playwright, BeautifulSoup, pandas
- **Warehouse:** DuckDB
- **Transformation & testing:** dbt (dbt-duckdb)
- **Orchestration:** Apache Airflow 3
- **Containerization:** Docker, Docker Compose
- **Visualization:** Tableau Public

## Data model

| Model | Grain | Description |
|---|---|---|
| `dim_event` | one row per event | Name, date, year, location, country |
| `dim_fighter` | one row per fighter | Most recent name, first/last UFC fight, total fights |
| `fct_fights` | one row per fight | Fighters, winner, weight class, method, round, duration |
| `fct_fighter_fights` | one row per fighter per fight | W/L/D/NC result, opponent; makes records and win rates a simple `GROUP BY` |

## Design decisions

- **Bot protection:** ufcstats.com serves a JavaScript challenge page to plain HTTP clients, so the scraper uses Playwright to drive a headless browser that passes the check before reading the page.
- **HTML caching / incremental loads:** every event page is saved to disk after the first download. Weekly runs only fetch new events, so a refresh takes seconds instead of ~30 minutes, and the site isn't re-scraped unnecessarily.
- **Polite scraping:** a 1.5-second delay between page requests.
- **Error isolation:** one failed event page is logged and skipped instead of failing the whole run.
- **Stable IDs over names:** fighters are keyed on UFCStats IDs, not names, which handles duplicate names and spelling changes. `dim_fighter` keeps each fighter's most recent spelling.
- **Standardized outcomes:** raw methods (U-DEC, S-DEC, M-DEC, KO/TKO, SUB, ...) are grouped into KO/TKO, Submission, Decision, Disqualification, and Other.
- **Isolated environments:** inside Docker, the pipeline runs in its own Python environment so its libraries never conflict with Airflow's.

## Data quality

dbt tests run after every refresh, and the pipeline stops if any fail:

- `unique` + `not_null` on every primary key (events, fights, fighters)
- `relationships`: every fight links to a real event, and every winner to a real fighter
- `accepted_values`: fighter results are only W, L, D, or NC

## How to run it

**Requirements:** Python 3.11+, Docker Desktop

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/ufc-pipeline.git
cd ufc-pipeline
```

**Option 1: run once, locally**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
python pipeline.py
```

**Option 2: scheduled with Airflow**
```bash
docker compose up --build -d
docker compose exec airflow cat /opt/airflow/simple_auth_manager_passwords.json.generated
```
Open http://localhost:8080, log in as `admin`, then unpause and trigger `ufc_pipeline`.

The first full scrape takes about 30 minutes; after that, refreshes take seconds.

## Project structure

```
ufc-pipeline/
├── scraper/
│   ├── events.py        # scrape the list of completed events
│   ├── fights.py        # scrape each event's fight card (cached)
│   ├── load.py          # load CSVs into DuckDB
│   └── export.py        # export marts to CSV for Tableau
├── transform/           # dbt project
│   └── models/
│       ├── staging/     # stg_events, stg_fights
│       └── marts/       # dims and facts
├── dags/
│   └── ufc_pipeline.py  # Airflow DAG
├── data/
│   ├── raw/             # scraped CSVs
│   └── exports/         # dashboard-ready CSVs
├── pipeline.py          # run every step once, in order
├── Dockerfile
└── docker-compose.yml
```

## Known limitations

- `fight_duration_seconds` assumes 5-minute rounds. Early UFC events had different round rules, so durations for the 1990s are approximate.
- Results are scraped from public pages, so a change to the site's HTML requires updating the scraper's selectors.
- The weekly schedule runs on a local machine and only fires while Docker is running.

## Roadmap

- [ ] Round-by-round fight stats (strikes, takedowns, control time)
- [ ] Move storage to AWS S3 + Snowflake
- [ ] CI with GitHub Actions to run dbt tests on every push

---

*Data source: [UFCStats](http://ufcstats.com). This is a personal portfolio project and is not affiliated with the UFC.*
