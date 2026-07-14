import sqlite3

def init_db():
    conn = sqlite3.connect("data/products.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT,
            url TEXT,
            ingredients TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_product(name, url, ingredients):
    conn = sqlite3.connect("data/products.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, url, ingredients) VALUES (?, ?, ?)",
                   (name, url, ",".join(ingredients)))
    conn.commit()
    conn.close()
def get_all_products():
  conn = sqlite3.connect("data/products.db")
  cursor = conn.cursor()
  cursor.execute("SELECT name, url, ingredients FROM products")
  rows = cursor.fetchall()
  conn.close()
  products = []
  for row in rows:
        products.append({
            "name": row[0],
            "url": row[1],
            "ingredients": row[2]
        })
  return products
init_db()
print("Database is ready!!!")