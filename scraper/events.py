import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from playwright.sync_api import sync_playwright

URL = "http://ufcstats.com/statistics/events/completed?page=all"


def fetch_page(url):
    """Open the page in a real (hidden) browser, wait for the table, return the HTML."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_selector("tr.b-statistics__table-row", timeout=60000)
        html = page.content()
        browser.close()
    return html


def parse_events(html):
    """Pull event name, date, location, and URL from the events table."""
    soup = BeautifulSoup(html, "html.parser")
    events = []

    for row in soup.select("tr.b-statistics__table-row"):
        link = row.select_one("a.b-link")
        if link is None:
            continue

        date_text = row.select_one("span.b-statistics__date").get_text(strip=True)
        cells = row.find_all("td")

        events.append({
            "event_id": link["href"].rstrip("/").split("/")[-1],
            "event_name": link.get_text(strip=True),
            "event_date": datetime.strptime(date_text, "%B %d, %Y").date(),
            "location": cells[1].get_text(strip=True),
            "event_url": link["href"],
        })

    return events


def main():
    html = fetch_page(URL)
    events = parse_events(html)

    if not events:
        raise SystemExit("No events found - check the selectors or the page HTML.")

    df = pd.DataFrame(events)
    df = df[df["event_date"] <= datetime.today().date()]
    df.to_csv("data/raw/events.csv", index=False)
    print(f"Saved {len(df)} events")
    print(df.head())


if __name__ == "__main__":
    main()