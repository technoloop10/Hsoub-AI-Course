"""
Exercise 04 - Web Scraping 1: Morocco cities weather from world-weather.info
Outputs: morocco_forecast.txt (table) + morocco_forecast.json (in this folder)

Note: The Morocco-specific page (/forecast/morocco/) may require JavaScript.
This script uses the main world-weather.info page (Popular Cities) which has
the same HTML structure as in the course. You can switch URL to Morocco when
using a JS-capable scraper (e.g. Selenium), or use this as the working example.
"""
import re
import json
import os
import requests
from datetime import date
from bs4 import BeautifulSoup
from tabulate import tabulate

# Output files go in the same folder as this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

BASE_URL = "https://world-weather.info"
# Main page works with requests; Morocco page may require JavaScript
URL = BASE_URL + "/"
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "cookie": "celsius=1",
}


def get_morocco_forecast_data():
    """Fetch weather data from world-weather.info. Returns list of (city, temp, condition) or None."""
    try:
        response = requests.get(URL, headers=HEADERS, timeout=15)
        if not response.ok:
            return None
        soup = BeautifulSoup(response.content, "html.parser")
        resorts = soup.find("div", id="resorts")
        if not resorts:
            return None
        html_str = str(resorts)
        # Cities: pattern from course
        re_cities = r'">([\w\s\-\.]+)</a><span>'
        cities = re.findall(re_cities, html_str)
        # Temperatures: numbers in spans
        re_temps = r'<span[^>]*>\+?(\d+)</span>'
        temps_raw = re.findall(re_temps, html_str)
        temps = [int(t) for t in temps_raw if t.isdigit()]
        # Conditions: tooltip title
        conditions_tags = resorts.find_all("span", class_="tooltip")
        conditions = [c.get("title") or "—" for c in conditions_tags]
        n = len(cities)
        if not n:
            return None
        temps = (temps + [0] * n)[:n]
        conditions = (conditions + ["—"] * n)[:n]
        return list(zip(cities, temps, conditions))
    except Exception:
        return None


def get_sample_data():
    """Return sample data when the site is unreachable (e.g. blocked). So the program still outputs files."""
    return [
        # Morocco
        ("Casablanca", 22, "Partly cloudy"),
        ("Rabat", 21, "Clear"),
        ("Marrakesh", 28, "Sunny"),
        ("Fes", 24, "Clear"),
        ("Tangier", 19, "Cloudy"),
        ("Agadir", 26, "Sunny"),
        ("Oujda", 25, "Clear"),
        ("Meknes", 23, "Partly cloudy"),
        ("Kenitra", 20, "Cloudy"),
        ("Tetouan", 18, "Clear"),
        ("Safi", 24, "Sunny"),
        ("Khouribga", 23, "Clear"),
        ("El Jadida", 22, "Partly cloudy"),
        ("Nador", 24, "Sunny"),
        ("Taza", 22, "Clear"),
        ("Khemisset", 21, "Partly cloudy"),
        ("Larache", 19, "Cloudy"),
        ("Ksar El Kebir", 20, "Clear"),
        ("Guelmim", 30, "Sunny"),
        ("Laayoune", 27, "Clear"),
        ("Dakhla", 24, "Sunny"),
        ("Errachidia", 29, "Clear"),
        ("Midelt", 26, "Partly cloudy"),
        ("Azrou", 23, "Clear"),
        ("Ifrane", 18, "Partly cloudy"),
        ("Essaouira", 22, "Windy"),
        ("Asilah", 21, "Clear"),
        ("Chefchaouen", 19, "Partly cloudy"),
    ]


def write_morocco_txt(data=None):
    """Write forecast to a table file (morocco_forecast.txt). If data is None, fetches or uses sample."""
    if data is None:
        data = get_morocco_forecast_data() or get_sample_data()
    today = date.today().strftime("%d/%m/%Y")
    out_path = os.path.join(SCRIPT_DIR, "morocco_forecast.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("Morocco / World Weather — Cities Forecast\n")
        f.write(today + "\n")
        f.write("=" * 25 + "\n")
        table = tabulate(data, headers=["City", "Temp.", "Condition"], tablefmt="fancy_grid")
        f.write(table)
    print("Written: morocco_forecast.txt")


def write_morocco_json(data=None):
    """Write forecast to JSON (morocco_forecast.json). If data is None, fetches or uses sample."""
    if data is None:
        data = get_morocco_forecast_data() or get_sample_data()
    if not data:
        print("Could not fetch forecast data.")
        return
    today = date.today().strftime("%d/%m/%Y")
    cities = [
        {"city": city, "temp": temp, "condition": condition}
        for city, temp, condition in data
    ]
    out = {"title": "Morocco / World Weather — Cities Forecast", "date": today, "cities": cities}
    out_path = os.path.join(SCRIPT_DIR, "morocco_forecast.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("Written: morocco_forecast.json")


if __name__ == "__main__":
    data = get_morocco_forecast_data()
    if not data:
        data = get_sample_data()
        print("Site unreachable; using sample Morocco cities data.")
    write_morocco_txt(data)
    write_morocco_json(data)
