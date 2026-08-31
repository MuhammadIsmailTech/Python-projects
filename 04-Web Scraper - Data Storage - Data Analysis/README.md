# P-4-WebScraperDataStorage

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](#license)

> Web scraper that collects product data from `books.toscrape.com` and stores it in CSV and SQLite formats.  
> This repository includes realistic sample data so the project is ready to explore and upload to GitHub.

## Overview

`P-4-WebScraperDataStorage` demonstrates a complete workflow:
- Scrape product information (title, price, availability, rating).
- Save raw results to `books.csv`.
- Store records in a local SQLite database `books.db`.
- Run basic analytics and save a summary `books_summary.csv`.

The repo includes sample data so reviewers can see outputs without running the scraper.

## Files

- `web_scraper.py` — Full scraper code (live scraping commented by default).
- `books.csv` — Sample dataset (ready to open in Excel).
- `books.db` — SQLite database containing the same sample rows.
- `books_summary.csv` — Small report for quick stats.
- `README.md` — This file.

## Quickstart

1. Clone this repository:
```bash
git clone https://github.com/Muhammadismail-gif/my-python-projects.git
cd P-4-WebScraperDataStorage
```

2. (Optional) Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # macOS / Linux
.venv\Scripts\activate    # Windows PowerShell
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Inspect sample data:
- Open `books.csv` with Excel or a text editor.
- Open `books_summary.csv` for summary stats.

5. (Optional) Run the live scraper:
> By default the live scraping call is commented to avoid accidental requests.  
Uncomment `scrape_pages(max_pages=5)` in `web_scraper.py` to run the scraper.

```bash
python web_scraper.py
```

## How it works (short)

- `requests` fetches HTML pages.
- `BeautifulSoup` parses HTML and extracts data using tag/classes.
- Data is written to CSV using Python's `csv` module.
- SQLite (`sqlite3`) stores structured rows in `books.db`.
- `pandas` is used for the summary analytics.

## Project Enhancements (suggested)

- Add pagination detection (stop when no "next" link).
- Add retries and exponential backoff for network errors.
- Add logging to a file instead of printing.
- Convert the pipeline into a small ETL script and schedule with cron or Task Scheduler.
- Build a Streamlit dashboard to visualize the scraped data.

## Requirements

Create a `requirements.txt` file with:
```
requests
beautifulsoup4
pandas
```

## License

MIT License — feel free to reuse and adapt.

---

**Author:** MuhammadIsmail-gif
