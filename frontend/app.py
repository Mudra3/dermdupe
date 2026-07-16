from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

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

def find_dupes(target_ingredients, all_products, threshold=0.5):
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
    dupes = find_dupes(ingredient_list, all_products)
    return render_template("results.html", dupes=dupes)

if __name__ == "__main__":
    app.run(debug=True)