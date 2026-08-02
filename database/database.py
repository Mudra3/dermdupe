import sqlite3

def init_db():
    conn = sqlite3.connect("data/products.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT,
            url TEXT,
            ingredients TEXT,
            category TEXT
        )
    """)
    
    
    try:
        cursor.execute("ALTER TABLE products ADD COLUMN category TEXT")
    except:
        pass
    
    conn.commit()
    conn.close()

def save_product(name, url, ingredients, category="unknown"):
    conn = sqlite3.connect("data/products.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM products WHERE url = ?", (url,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO products (name, url, ingredients, category) VALUES (?, ?, ?, ?)",
                       (name, url, ",".join(ingredients), category))
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
