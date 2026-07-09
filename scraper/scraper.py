import requests
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database import save_product
#connecting the scraper to the database



from bs4 import BeautifulSoup

def scrape_product(url):
 response = requests.get(url) 
 soup = BeautifulSoup(response.text, "html.parser")
#getting product name
 name= soup.find("h1").text.strip()
#getting all th ingredients
 ingredient_tags = soup.find_all("a", class_="ingred-link")

 ingredients= [tag.text.strip() for tag in ingredient_tags]
 return{
    "name" : name,
    "ingredients" : ingredients

}
result = scrape_product("https://incidecoder.com/products/vanicream-moisturizer")
save_product(result["name"], "https://incidecoder.com/products/vanicream-moisturizer", result["ingredients"])
print("Saved:", result["name"])

