import sqlite3

conn = sqlite3.connect("ecommerce.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price REAL,
    description TEXT,
    image TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    password TEXT
)
""")

cur.execute("""
INSERT INTO products (name, price, description, image)
VALUES
('Red Shoes', 2500, 'Comfortable running shoes.', 'sample-product.png'),
('Smart Watch', 3500, 'Fitness tracking smartwatch.', 'sample-product.png'),
('Headphones', 1800, 'Noise cancelling headphones.', 'sample-product.png')
""")

conn.commit()
conn.close()

print("Database created.")
