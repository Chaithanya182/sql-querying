"""
Seed script to create and populate a sample e-commerce SQLite database.
Run: python seed_db.py
"""

import sqlite3
import os
import random
from datetime import datetime, timedelta

DB_DIR = os.path.join(os.path.dirname(__file__), "data")
DB_PATH = os.path.join(DB_DIR, "sample.db")


def create_database():
    os.makedirs(DB_DIR, exist_ok=True)

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # ── Tables ──────────────────────────────────────────────
    cursor.executescript("""
        CREATE TABLE categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT
        );

        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category_id INTEGER NOT NULL,
            price REAL NOT NULL,
            stock_quantity INTEGER NOT NULL DEFAULT 0,
            rating REAL DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        );

        CREATE TABLE customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            city TEXT,
            country TEXT DEFAULT 'India',
            joined_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            total_amount REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        );

        CREATE TABLE order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        );

        CREATE TABLE reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            customer_id INTEGER NOT NULL,
            rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
            comment TEXT,
            review_date TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id),
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        );
    """)

    # ── Seed Data ───────────────────────────────────────────
    categories = [
        ("Electronics", "Gadgets, devices, and accessories"),
        ("Clothing", "Apparel and fashion items"),
        ("Books", "Fiction, non-fiction, and textbooks"),
        ("Home & Kitchen", "Furniture, cookware, and decor"),
        ("Sports", "Sports equipment and accessories"),
        ("Beauty", "Skincare, makeup, and personal care"),
    ]
    cursor.executemany("INSERT INTO categories (name, description) VALUES (?, ?)", categories)

    products_data = [
        # Electronics
        ("Wireless Earbuds Pro", 1, 2499.00, 150, 4.5),
        ("Smartphone X12", 1, 18999.00, 45, 4.3),
        ("Laptop UltraSlim", 1, 54999.00, 20, 4.7),
        ("Bluetooth Speaker", 1, 1299.00, 200, 4.1),
        ("Smart Watch S3", 1, 3999.00, 80, 4.4),
        ("USB-C Hub Adapter", 1, 899.00, 300, 4.2),
        ("Mechanical Keyboard", 1, 2799.00, 65, 4.6),
        ("Wireless Mouse", 1, 599.00, 400, 4.0),
        # Clothing
        ("Cotton T-Shirt", 2, 499.00, 500, 4.2),
        ("Denim Jacket", 2, 2199.00, 60, 4.5),
        ("Running Shoes", 2, 3499.00, 100, 4.6),
        ("Formal Shirt", 2, 1299.00, 150, 4.1),
        ("Hoodie Classic", 2, 1599.00, 120, 4.3),
        # Books
        ("Python Programming", 3, 599.00, 200, 4.8),
        ("Data Structures & Algorithms", 3, 699.00, 150, 4.7),
        ("Machine Learning Basics", 3, 899.00, 80, 4.5),
        ("Web Dev Bootcamp", 3, 499.00, 250, 4.4),
        ("Clean Code", 3, 749.00, 100, 4.9),
        # Home & Kitchen
        ("Non-stick Pan Set", 4, 1899.00, 70, 4.3),
        ("Coffee Maker", 4, 4999.00, 30, 4.6),
        ("LED Desk Lamp", 4, 799.00, 180, 4.4),
        ("Storage Organizer", 4, 599.00, 220, 4.1),
        # Sports
        ("Yoga Mat Premium", 5, 999.00, 150, 4.5),
        ("Resistance Bands Set", 5, 699.00, 200, 4.3),
        ("Cricket Bat Pro", 5, 2499.00, 40, 4.7),
        ("Football Official", 5, 1199.00, 90, 4.4),
        # Beauty
        ("Sunscreen SPF50", 6, 399.00, 300, 4.6),
        ("Face Wash Gel", 6, 249.00, 400, 4.2),
        ("Moisturizer Cream", 6, 549.00, 250, 4.5),
        ("Hair Serum", 6, 449.00, 180, 4.3),
    ]
    cursor.executemany(
        "INSERT INTO products (name, category_id, price, stock_quantity, rating) VALUES (?, ?, ?, ?, ?)",
        products_data,
    )

    first_names = ["Aarav", "Priya", "Rohan", "Ananya", "Vikram", "Sneha", "Arjun", "Kavya",
                    "Rahul", "Meera", "Aditya", "Ishita", "Karan", "Divya", "Nikhil",
                    "Pooja", "Siddharth", "Riya", "Amit", "Neha"]
    last_names = ["Sharma", "Patel", "Kumar", "Singh", "Gupta", "Reddy", "Joshi", "Verma",
                  "Iyer", "Nair", "Rao", "Das", "Mehta", "Shah", "Chopra",
                  "Malhotra", "Bose", "Dutta", "Pillai", "Menon"]
    cities = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Pune",
              "Ahmedabad", "Jaipur", "Lucknow"]

    customers_data = []
    for i in range(20):
        fn = first_names[i]
        ln = last_names[i]
        email = f"{fn.lower()}.{ln.lower()}@email.com"
        city = random.choice(cities)
        joined = (datetime.now() - timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d")
        customers_data.append((fn, ln, email, city, "India", joined))

    cursor.executemany(
        "INSERT INTO customers (first_name, last_name, email, city, country, joined_at) VALUES (?, ?, ?, ?, ?, ?)",
        customers_data,
    )

    # Orders & Order Items
    statuses = ["completed", "completed", "completed", "shipped", "pending", "cancelled"]
    order_id = 1
    for _ in range(50):
        cust_id = random.randint(1, 20)
        order_date = (datetime.now() - timedelta(days=random.randint(1, 180))).strftime("%Y-%m-%d")
        status = random.choice(statuses)

        num_items = random.randint(1, 4)
        prod_ids = random.sample(range(1, 31), num_items)
        total = 0.0
        items = []
        for pid in prod_ids:
            qty = random.randint(1, 3)
            price = products_data[pid - 1][2]
            items.append((order_id, pid, qty, price))
            total += qty * price

        cursor.execute(
            "INSERT INTO orders (customer_id, order_date, total_amount, status) VALUES (?, ?, ?, ?)",
            (cust_id, order_date, round(total, 2), status),
        )
        cursor.executemany(
            "INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)",
            items,
        )
        order_id += 1

    # Reviews
    reviews_data = []
    for _ in range(60):
        pid = random.randint(1, 30)
        cid = random.randint(1, 20)
        rating = random.randint(3, 5)
        comments = [
            "Great product, highly recommend!",
            "Good quality for the price.",
            "Exceeded my expectations.",
            "Decent product, could be better.",
            "Amazing! Will buy again.",
            "Fast delivery and great packaging.",
            "Value for money.",
            "Loved it, perfect for daily use.",
        ]
        comment = random.choice(comments)
        review_date = (datetime.now() - timedelta(days=random.randint(1, 120))).strftime("%Y-%m-%d")
        reviews_data.append((pid, cid, rating, comment, review_date))

    cursor.executemany(
        "INSERT INTO reviews (product_id, customer_id, rating, comment, review_date) VALUES (?, ?, ?, ?, ?)",
        reviews_data,
    )

    conn.commit()
    conn.close()
    print(f"✅ Sample database created at: {DB_PATH}")
    print(f"   - 6 categories, 30 products, 20 customers")
    print(f"   - 50 orders, ~100+ order items, 60 reviews")


if __name__ == "__main__":
    create_database()
