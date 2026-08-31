import requests
from bs4 import BeautifulSoup
import csv
import sqlite3
import time
import pandas as pd

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

def scrape_pages(max_pages=5, delay=1.5, save_csv="books.csv", save_db="books.db"):
    all_books = []
    for page in range(1, max_pages + 1):
        print(f"Scraping Page {page} ...")
        try:
            url = BASE_URL.format(page)
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        books = soup.find_all('article', class_='product_pod')

        if not books:
            print("No more books found. Stopping.")
            break

        for book in books:
            title = book.h3.a['title']
            price_text = book.find('p', class_='price_color').text.strip()
            price = float(price_text.replace('£', '').replace('Â',''))
            availability = book.find('p', class_='instock availability').text.strip()
            rating = book.p['class'][1]

            all_books.append((title, price, availability, rating))

        time.sleep(delay)

    # Save to CSV
    with open(save_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Title', 'Price', 'Availability', 'Rating'])
        writer.writerows(all_books)
    print(f"✅ Data saved to {save_csv}")

    # Save to SQLite
    conn = sqlite3.connect(save_db)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS books (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        price REAL,
                        availability TEXT,
                        rating TEXT
                    )""")
    cursor.executemany("INSERT INTO books (title, price, availability, rating) VALUES (?, ?, ?, ?)", all_books)
    conn.commit()
    conn.close()
    print(f"✅ Data saved to {save_db}")

    return all_books

def analyze(csv_file="books.csv", summary_file="books_summary.csv"):
    df = pd.read_csv(csv_file)
    summary = {
        "Total Books": [len(df)],
        "Average Price": [df['Price'].mean()],
        "Highest Price": [df['Price'].max()],
        "Lowest Price": [df['Price'].min()]
    }
    summary_df = pd.DataFrame(summary)
    summary_df.to_csv(summary_file, index=False)
    print(f"✅ Analysis summary saved to {summary_file}")
    print(summary_df.to_string(index=False))

if __name__ == "__main__":
    # Default behavior: do not run live scrape when distributed on GitHub.
    # To run a live scrape, uncomment the line below:
    # scrape_pages(max_pages=5)
    
    # Instead, the repo includes sample data (books.csv) for immediate use.
    print("This repository includes sample data (books.csv).")
    print("If you want to run the live scraper, edit this file and call scrape_pages(max_pages=5).")
