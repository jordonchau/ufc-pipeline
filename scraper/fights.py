import time
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

EVENTS_CSV = "data/raw/events.csv"
OUTPUT_CSV = "data/raw/fights.csv"
HTML_DIR = Path("data/raw/html/events")
TEST_LIMIT = None
DELAY_SECONDS = 1.5

def get_event_html(page, event_id, url):
    """Return the event page HTML, using the saved copy if we already downloaded it."""
    cache_file = HTML_DIR / f"{event_id}.html"
    if cache_file.exists():
        return cache_file.read_text(encoding="utf-8")

    page.goto(url, timeout=60000)
    page.wait_for_selector("tr.b-fight-details__table-row", timeout=60000)
    html = page.content()
    cache_file.write_text(html, encoding="utf-8")
    time.sleep(DELAY_SECONDS)
    return html


def text(el):
    """Get clean text from an element, or None if it doesn't exist."""
    return el.get_text(" ", strip=True) if el else None


def parse_fights(html, event_id):
    """Pull every fight from one event page."""
    soup = BeautifulSoup(html, "html.parser")
    fights = []

    rows = soup.select("tr.b-fight-details__table-row[data-link]")
    for order, row in enumerate(rows, start=1):
        cols = row.find_all("td")
        fighters = cols[1].select("a")
        method = cols[7].select("p")
        result = (text(cols[0]) or "").lower()

        if "win" in result:
            outcome = "win"            # first fighter listed is the winner
        elif "draw" in result:
            outcome = "draw"
        elif "nc" in result:
            outcome = "no contest"
        else:
            outcome = None

        fights.append({
            "fight_id": row["data-link"].rstrip("/").split("/")[-1],
            "event_id": event_id,
            "bout_order": order,       # 1 = main event
            "fighter_1": text(fighters[0]),
            "fighter_1_id": fighters[0]["href"].rstrip("/").split("/")[-1],
            "fighter_2": text(fighters[1]),
            "fighter_2_id": fighters[1]["href"].rstrip("/").split("/")[-1],
            "outcome": outcome,
            "winner": text(fighters[0]) if outcome == "win" else None,
            "weight_class": text(cols[6]),
            "method": text(method[0]) if method else None,
            "method_detail": text(method[1]) if len(method) > 1 else None,
            "round": text(cols[8]),
            "time": text(cols[9]),
            "fight_url": row["data-link"],
        })

    return fights


def main():
    HTML_DIR.mkdir(parents=True, exist_ok=True)
    events = pd.read_csv(EVENTS_CSV)
    if TEST_LIMIT:
        events = events.head(TEST_LIMIT)

    all_fights = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()      # reuse one tab for every event

        for i, event in enumerate(events.itertuples(), start=1):
            try:
                html = get_event_html(page, event.event_id, event.event_url)
                fights = parse_fights(html, event.event_id)
                all_fights.extend(fights)
                print(f"[{i}/{len(events)}] {event.event_name}: {len(fights)} fights")
            except Exception as e:
                print(f"[{i}/{len(events)}] FAILED {event.event_name}: {e}")

        browser.close()

    df = pd.DataFrame(all_fights)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Saved {len(df)} fights")
    print(df.head())


if __name__ == "__main__":
    main()