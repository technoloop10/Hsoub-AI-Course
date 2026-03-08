"""
Exercise 05 - Web Scraping 2: Books from books.toscrape.com
Outputs: books.txt (table) + books.json (in this folder)
"""
import json
import os
from urllib.parse import urljoin
import requests
from datetime import date
from bs4 import BeautifulSoup
from tabulate import tabulate

# Output files go in the same folder as this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

BASE_URL = "https://books.toscrape.com"
CATALOGUE_URL = f"{BASE_URL}/catalogue"
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}


def get_book_category(book_url):
    """Fetch a book's product page and return its catalogue/category name from the breadcrumb."""
    try:
        if not book_url.startswith("http"):
            book_url = BASE_URL + "/" + book_url.lstrip("/")
        resp = requests.get(book_url, headers=HEADERS, timeout=10)
        if not resp.ok:
            return "—"
        soup = BeautifulSoup(resp.content, "html.parser")
        breadcrumb = soup.find("ul", class_="breadcrumb")
        if not breadcrumb:
            return "—"
        links = breadcrumb.find_all("a")
        # Breadcrumb: Home, Books, Category (index 2)
        if len(links) >= 3:
            return links[2].get_text(strip=True) or "—"
        return "—"
    except Exception:
        return "—"


def get_books_data(max_pages=1, fetch_category=True):
    """
    Fetch books from books.toscrape.com. Returns list of (title, price, availability, category).
    max_pages: number of catalogue pages to scrape (default 1).
    fetch_category: if True, fetch each book page to get catalogue/category name (slower).
    """
    books = []
    for page in range(1, max_pages + 1):
        url = f"{CATALOGUE_URL}/page-{page}.html"
        try:
            response = requests.get(url, headers=HEADERS, timeout=15)
            if not response.ok:
                continue
            soup = BeautifulSoup(response.content, "html.parser")
            articles = soup.find_all("article", class_="product_pod")
            for art in articles:
                # Title and link: h3 > a
                h3 = art.find("h3")
                title = ""
                book_href = ""
                if h3 and h3.find("a"):
                    a = h3.find("a")
                    title = a.get("title") or h3.get_text(strip=True)
                    book_href = a.get("href", "")
                # Price: p.price_color
                price_el = art.find("p", class_="price_color")
                price = price_el.get_text(strip=True) if price_el else "—"
                # Availability: p.instock / .availability
                avail_el = art.find("p", class_="instock") or art.find("p", class_="availability")
                availability = avail_el.get_text(strip=True) if avail_el else "—"
                # Category: fetch from product page (breadcrumb)
                category = "—"
                if fetch_category and book_href:
                    page_url = f"{CATALOGUE_URL}/page-{page}.html"
                    full_url = urljoin(page_url, book_href)
                    category = get_book_category(full_url)
                books.append((title, price, availability, category))
        except Exception:
            continue
    return books


def write_books_txt(max_pages=1, fetch_category=True):
    """Write books to a table file (books.txt)."""
    data = get_books_data(max_pages=max_pages, fetch_category=fetch_category)
    if not data:
        print("Could not fetch books data.")
        return
    today = date.today().strftime("%d/%m/%Y")
    out_path = os.path.join(SCRIPT_DIR, "books.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("Books to Scrape — Catalog\n")
        f.write(today + "\n")
        f.write("=" * 30 + "\n")
        table = tabulate(data, headers=["Title", "Price", "Availability", "Category"], tablefmt="fancy_grid")
        f.write(table)
    print("Written: books.txt")


def write_books_json(max_pages=1, fetch_category=True):
    """Write books to JSON (books.json)."""
    data = get_books_data(max_pages=max_pages, fetch_category=fetch_category)
    if not data:
        print("Could not fetch books data.")
        return
    today = date.today().strftime("%d/%m/%Y")
    books_list = [
        {"title": title, "price": price, "availability": availability, "category": category}
        for title, price, availability, category in data
    ]
    out = {"title": "Books to Scrape — Catalog", "date": today, "books": books_list}
    out_path = os.path.join(SCRIPT_DIR, "books.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("Written: books.json")


if __name__ == "__main__":
    # First page only by default; set max_pages=50 for full catalog
    # fetch_category=True gets each book's category from its product page (slower)
    write_books_txt(max_pages=1, fetch_category=True)
    write_books_json(max_pages=1, fetch_category=True)
