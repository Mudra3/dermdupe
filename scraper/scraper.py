import requests
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.database import save_product
from bs4 import BeautifulSoup

def scrape_product(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    name = soup.find("h1").text.strip().replace("\n", " ").strip()
    ingredient_tags = soup.find_all("a", class_="ingred-link")
    ingredients = [tag.text.strip().replace("\n", "").strip() for tag in ingredient_tags]
    return {
        "name": name,
        "ingredients": ingredients
    }

def get_product_urls(search_url):
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a", class_="simpletextlistitem")
    urls = []
    for link in links:
        href = link.get("href")
        full_url = "https://incidecoder.com" + href
        urls.append(full_url)
    return urls

search_queries = [
    "moisturizer",
    "serum",
    "sunscreen",
    "toner",
    "cleanser",
    "eye cream",
    "face oil",
    "exfoliant"
]

for query in search_queries:
    print(f"\nScraping: {query}")
    search_url = f"https://incidecoder.com/search?query={query}"
    urls = get_product_urls(search_url)
    print(f"Found {len(urls)} products")
    for url in urls:
        try:
            result = scrape_product(url)
            save_product(result["name"], url, result["ingredients"])
            print("Saved:", result["name"])
        except Exception as e:
            print(f"Skipped {url}: {e}")