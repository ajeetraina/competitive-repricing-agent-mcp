#!/usr/bin/env python3
"""
Competitive Intelligence Agent - Database Initialization
=========================================================
This script creates a SQLite database with 30 days of historical price data.

WHY THIS MATTERS (vs ChatGPT):
- ChatGPT forgets everything between sessions
- This database PERSISTS - you can query it tomorrow, next week, next month
- Real trend analysis requires historical data that survives conversations
"""

import sqlite3
import random
from datetime import datetime, timedelta
import os

# Database path
DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, '..', 'data', 'price_intelligence.db')

def create_database():
    """Create the database schema"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Enable WAL mode for better performance
    cursor.execute("PRAGMA journal_mode=WAL")
    
    # Products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            category TEXT,
            brand TEXT,
            msrp REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Price history table - THE KEY TO PERSISTENCE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            competitor TEXT NOT NULL,
            price REAL NOT NULL,
            original_price REAL,
            discount_percent REAL,
            in_stock BOOLEAN DEFAULT 1,
            url TEXT,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    ''')
    
    # Price alerts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS price_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            competitor TEXT,
            alert_type TEXT NOT NULL,
            old_price REAL,
            new_price REAL,
            change_percent REAL,
            message TEXT,
            acknowledged BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    ''')
    
    # Create indexes for fast queries
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_price_history_product ON price_history(product_id, scraped_at DESC)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_price_history_competitor ON price_history(competitor)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_price_history_date ON price_history(scraped_at)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_alerts_product ON price_alerts(product_id, created_at DESC)')
    
    conn.commit()
    print("✅ Database schema created successfully!")
    return conn

def generate_realistic_price_history(base_price, days=30, volatility=0.02):
    """Generate realistic price movements over time"""
    prices = []
    current_price = base_price * random.uniform(1.05, 1.15)  # Start higher
    
    for day in range(days, 0, -1):
        # Add some randomness but trend downward toward holiday season
        daily_change = random.gauss(0, volatility)
        trend = -0.002 if day < 14 else -0.001  # Accelerate drops near holidays
        
        # Occasional bigger drops (sales events)
        if random.random() < 0.1:
            daily_change -= random.uniform(0.02, 0.05)
        
        current_price = current_price * (1 + daily_change + trend)
        current_price = max(current_price, base_price * 0.70)  # Floor at 30% off
        
        date = datetime.now() - timedelta(days=day)
        prices.append((date.isoformat(), round(current_price, 2)))
    
    return prices

def populate_sample_data(conn):
    """Populate with 30 days of realistic price data"""
    cursor = conn.cursor()
    
    # Sample products to monitor
    products = [
        ('MBA-M3-256', 'MacBook Air M3 256GB', 'Laptops', 'Apple', 1099),
        ('MBA-M3-512', 'MacBook Air M3 512GB', 'Laptops', 'Apple', 1299),
        ('MBP-M3-PRO', 'MacBook Pro 14" M3 Pro', 'Laptops', 'Apple', 1999),
        ('IPAD-PRO-11', 'iPad Pro 11" M4', 'Tablets', 'Apple', 999),
        ('AIRPODS-PRO', 'AirPods Pro 2nd Gen', 'Audio', 'Apple', 249),
        ('PS5-SLIM', 'PlayStation 5 Slim', 'Gaming', 'Sony', 499),
        ('XBOX-X', 'Xbox Series X', 'Gaming', 'Microsoft', 499),
        ('SWITCH-OLED', 'Nintendo Switch OLED', 'Gaming', 'Nintendo', 349),
    ]
    
    competitors = ['Amazon', 'Walmart', 'Best Buy', 'Target', 'Costco']
    
    # Insert products
    for sku, name, category, brand, msrp in products:
        cursor.execute('''
            INSERT OR IGNORE INTO products (sku, name, category, brand, msrp)
            VALUES (?, ?, ?, ?, ?)
        ''', (sku, name, category, brand, msrp))
    
    conn.commit()
    
    # Get product IDs
    cursor.execute('SELECT id, sku, msrp FROM products')
    product_data = cursor.fetchall()
    
    print(f"\n📦 Populating 30 days of price history for {len(product_data)} products...")
    
    total_records = 0
    alerts_generated = 0
    
    for product_id, sku, msrp in product_data:
        for competitor in competitors:
            # Each competitor has slightly different base pricing
            competitor_base = msrp * random.uniform(0.85, 0.95)
            prices = generate_realistic_price_history(competitor_base, days=30)
            
            prev_price = None
            for date, price in prices:
                # Calculate discount from MSRP
                discount = ((msrp - price) / msrp) * 100
                
                # Random stock status (mostly in stock)
                in_stock = random.random() > 0.05
                
                cursor.execute('''
                    INSERT INTO price_history 
                    (product_id, competitor, price, original_price, discount_percent, in_stock, scraped_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (product_id, competitor, price, msrp, round(discount, 1), in_stock, date))
                
                total_records += 1
                
                # Generate alerts for significant price drops (>5%)
                if prev_price and prev_price > 0:
                    change_pct = ((price - prev_price) / prev_price) * 100
                    if change_pct < -5:
                        cursor.execute('''
                            INSERT INTO price_alerts 
                            (product_id, competitor, alert_type, old_price, new_price, change_percent, message, created_at)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            product_id, competitor, 'PRICE_DROP',
                            prev_price, price, round(change_pct, 1),
                            f"Price dropped {abs(round(change_pct, 1))}% from ${prev_price} to ${price}",
                            date
                        ))
                        alerts_generated += 1
                
                prev_price = price
    
    conn.commit()
    
    print(f"✅ Inserted {total_records:,} price records")
    print(f"🚨 Generated {alerts_generated} price alerts")
    
    return total_records, alerts_generated

def show_database_stats(conn):
    """Display database statistics"""
    cursor = conn.cursor()
    
    print("\n" + "="*60)
    print("📊 DATABASE STATISTICS")
    print("="*60)
    
    cursor.execute('SELECT COUNT(*) FROM products')
    print(f"Products tracked: {cursor.fetchone()[0]}")
    
    cursor.execute('SELECT COUNT(*) FROM price_history')
    print(f"Price history records: {cursor.fetchone()[0]:,}")
    
    cursor.execute('SELECT MIN(scraped_at), MAX(scraped_at) FROM price_history')
    min_date, max_date = cursor.fetchone()
    print(f"Date range: {min_date[:10]} to {max_date[:10]}")
    
    cursor.execute('SELECT DISTINCT competitor FROM price_history')
    competitors = [row[0] for row in cursor.fetchall()]
    print(f"Competitors: {', '.join(competitors)}")
    
    cursor.execute('SELECT COUNT(*) FROM price_alerts WHERE acknowledged = 0')
    print(f"Unacknowledged alerts: {cursor.fetchone()[0]}")
    
    print("="*60)

if __name__ == '__main__':
    print("🚀 Competitive Intelligence Agent - Database Initialization")
    print("="*60)
    print("WHY MCP MATTERS: This data PERSISTS between conversations!")
    print("ChatGPT would forget all this the moment you close the tab.")
    print("="*60 + "\n")
    
    conn = create_database()
    records, alerts = populate_sample_data(conn)
    show_database_stats(conn)
    
    conn.close()
    print(f"\n✅ Database ready at: {DB_PATH}")
    print("🔑 This database will persist for future queries!")
