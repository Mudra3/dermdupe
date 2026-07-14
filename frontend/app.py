from flask import Flask, render_template, request 
import sys 
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.database import get_all_products
from matcher.similarity import find_dupes
app= Flask(__name__)

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
    app.run(debug= True)
    