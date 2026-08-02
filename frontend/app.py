from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

def get_ingredients_from_description(description):
    description = description.lower()
    ingredients = []
    if any(word in description for word in ["hydrating", "moisture", "dry skin"]):
        ingredients += ["Glycerin", "Hyaluronic Acid", "Squalane", "Ceramide NP"]
    if any(word in description for word in ["brightening", "glow", "vitamin c"]):
        ingredients += ["Niacinamide", "Ascorbic Acid", "Kojic Acid"]
    if any(word in description for word in ["anti aging", "wrinkle", "retinol"]):
        ingredients += ["Retinol", "Peptides", "Collagen", "Adenosine"]
    if any(word in description for word in ["acne", "oily", "pores", "breakout"]):
        ingredients += ["Salicylic Acid", "Niacinamide", "Zinc", "Tea Tree"]
    if any(word in description for word in ["sensitive", "calm", "redness"]):
        ingredients += ["Centella Asiatica", "Aloe Vera", "Ceramide EOP", "Panthenol"]
    if not ingredients:
        ingredients = ["Glycerin", "Water", "Niacinamide"]
    return ingredients

def get_all_products():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'products.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name, url, ingredients FROM products")
    rows = cursor.fetchall()
    conn.close()
    return [{"name": r[0], "url": r[1], "ingredients": r[2]} for r in rows]

def jaccard_similarity(list1, list2):
    set1 = set([i.lower() for i in list1])
    set2 = set([i.lower() for i in list2])
    intersection = set1 & set2
    union = set1 | set2
    if len(union) == 0:
        return 0
    return len(intersection) / len(union)

def find_dupes(target_ingredients, all_products, threshold=0.1):
    dupes = []
    for product in all_products:
        ingredients = product["ingredients"].split(",")
        score = jaccard_similarity(target_ingredients, ingredients)
        if score >= threshold:
            dupes.append({"name": product["name"], "score": round(score * 100, 2)})
    return dupes

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    ingredients = request.form.get("ingredients")
    ingredient_list = [i.strip() for i in ingredients.split(",")]
    all_products = get_all_products()
    dupes = sorted(find_dupes(ingredient_list, all_products), key=lambda x: x["score"], reverse=True)
    return render_template("results.html", dupes=dupes)

@app.route("/product-search", methods=["POST"])
def product_search():
    product_name = request.form.get("product_name")
    
    try:
        import requests as req
        from bs4 import BeautifulSoup
        
        search_url = f"https://incidecoder.com/search?query={product_name.replace(' ', '+')}"
        response = req.get(search_url)
        soup = BeautifulSoup(response.text, "html.parser")
        first_result = soup.find("a", class_="simpletextlistitem")
        
        if not first_result:
            return render_template("results.html", dupes=[])
        
        product_url = "https://incidecoder.com" + first_result.get("href")
        product_response = req.get(product_url)
        product_soup = BeautifulSoup(product_response.text, "html.parser")
        ingredient_tags = product_soup.find_all("a", class_="ingred-link")
        ingredient_list = [tag.text.strip().replace("\n", "").strip() for tag in ingredient_tags]
        
        if not ingredient_list:
            return render_template("results.html", dupes=[])
        
        all_products = get_all_products()
        dupes = sorted(find_dupes(ingredient_list, all_products), key=lambda x: x["score"], reverse=True)
        return render_template("results.html", dupes=dupes)
    
    except Exception as e:
        print(f"Error: {e}")
        return render_template("results.html", dupes=[])
    
    if not result:
        return render_template("results.html", dupes=[], error="Product not found on INCI Decoder")
    
    ingredient_list = result["ingredients"]
    all_products = get_all_products()
    dupes = sorted(find_dupes(ingredient_list, all_products), key=lambda x: x["score"], reverse=True)
    
    return render_template("results.html", dupes=dupes, searched_product=result["name"])
if __name__ == "__main__":
    app.run(debug=True)