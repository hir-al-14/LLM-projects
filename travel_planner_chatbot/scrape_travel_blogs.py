# to fetch and return content in a structured sections format from the Wikivoyage page's MediaWiki API
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

def get_page_section(city):
    url = "https://en.wikivoyage.org/w/api.php"
    params = {
        "action": "parse",
        "page": city,
        "format": "json",
        "prop": "text"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    html = response.json()["parse"]["text"]["*"] # Note - response.json (to convert http response to python dictionary), * (entire html of the parsed page)
    soup = BeautifulSoup(html, "html.parser")

    content = {}
    current_section = "Introduction"
    content[current_section] = ""

    for text in soup.find_all(["h2", "p", "ul"]):
        if text.name == "h2":
            title_name = text.get_text().replace("[edit]", "").strip()
            current_section = title_name
            content[current_section] = ""
        else:
            content[current_section] += text.get_text().strip() + "\n"

    return content

def save_to_csv(city_region_list, output_csv="data/travel_data.csv"):
    all_rows = []

    for city, region in city_region_list:
        print(f"Fetching {city} ({region})")
        content = get_page_section(city)
        time.sleep(2)
        if content:
            for section, text in content.items():
                all_rows.append({
                    "city": city,
                    "region": region,
                    "section": section,
                    "text": text.strip()
                })
                
    df = pd.DataFrame(all_rows)
    os.makedirs("data", exist_ok=True)
    df.to_csv(output_csv, index=False)
    print(f"Saved {len(df)} rows to {output_csv}")

if __name__ == "__main__":
    cities = [
        ("Kyoto", "Asia"),
        ("Tokyo", "Asia"),
        ("Paris", "Europe"),
        ("Barcelona", "Europe"),
        ("Berlin", "Europe"),
        ("New York City", "USA"),
        ("Chicago", "USA"),
        ("San Francisco", "USA"),
        ("Bangkok", "Asia"),
        ("Bali", "Asia"),
        ("Rome", "Europe"),
        ("Amsterdam", "Europe"),
        ("Istanbul", "Europe"),
        ("Los Angeles", "USA"),
        ("Miami", "USA"),
        ("Hanoi", "Asia"),
        ("Lisbon", "Europe"),
        ("Vienna", "Europe"),
        ("Seoul", "Asia"),
        ("Prague", "Europe"),
    ]

    save_to_csv(cities)
