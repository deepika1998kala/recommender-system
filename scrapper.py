import json
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.shl.com/solutions/products/product-catalog/"


def scrape_catalog():
    response = requests.get(BASE_URL)

    soup = BeautifulSoup(response.text, "html.parser")

    assessments = []

    cards = soup.find_all("a")

    visited = set()

    for card in cards:
        href = card.get("href")

        if not href:
            continue

        if "/products/" not in href:
            continue

        full_url = href

        if full_url.startswith("/"):
            full_url = "https://www.shl.com" + full_url

        if full_url in visited:
            continue

        visited.add(full_url)

        name = card.get_text(strip=True)

        if not name:
            continue

        assessments.append(
            {
                "name": name,
                "url": full_url,
                "description": name,
                "test_type": "Unknown",
            }
        )

    with open("catalog.json", "w") as f:
        json.dump(assessments, f, indent=2)

    print(f"Saved {len(assessments)} assessments")


if __name__ == "__main__":
    scrape_catalog()