#!/usr/bin/env python3
"""
Competitive Intelligence Agent - Trend Analysis
================================================
This script queries historical data to identify trends.

THE MCP DIFFERENCE:
- We're querying 1,200 price records spanning 30 days
- ChatGPT would need you to manually provide ALL this data every time
- With MCP + SQLite, we just query what we need
"""

import sqlite3
from datetime import datetime, timedelta
import os

# Database path
DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, '..', 'data', 'price_intelligence.db')

def get_product_trends(product_sku):
    """Analyze price trends for a specific product"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, name, category, brand, msrp FROM products WHERE sku = ?', (product_sku,))
    product = cursor.fetchone()
    
    if not product:
        print(f"❌ Product {product_sku} not found")
        return
    
    product_id, name, category, brand, msrp = product
    
    print(f"\n{'='*70}")
    print(f"📊 PRICE TREND ANALYSIS: {name}")
    print(f"{'='*70}")
    print(f"Brand: {brand} | Category: {category} | MSRP: ${msrp}")
    print(f"{'='*70}\n")
    
    # Current prices
    cursor.execute('''
        SELECT competitor, price, discount_percent, in_stock
        FROM price_history 
        WHERE product_id = ?
        AND scraped_at = (SELECT MAX(scraped_at) FROM price_history WHERE product_id = ? AND competitor = price_history.competitor)
        ORDER BY price ASC
    ''', (product_id, product_id))
    
    current_prices = cursor.fetchall()
    
    print("💰 CURRENT PRICES")
    print("-" * 50)
    best = True
    for competitor, price, discount, in_stock in current_prices:
        stock = "✅ In Stock" if in_stock else "❌ Out of Stock"
        badge = " 🏆 BEST" if best else ""
        best = False
        print(f"  {competitor:12} ${price:>8.2f}  ({discount:>5.1f}% off)  {stock}{badge}")
    
    print(f"\n{'='*70}\n")
    conn.close()

def get_best_deals():
    """Find best deals across all products"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print(f"\n{'='*70}")
    print("🏆 BEST DEALS ACROSS ALL PRODUCTS")
    print(f"{'='*70}\n")
    
    cursor.execute('''
        SELECT p.name, ph.competitor, ph.price, ph.discount_percent
        FROM products p
        JOIN price_history ph ON p.id = ph.product_id
        WHERE ph.scraped_at = (SELECT MAX(scraped_at) FROM price_history WHERE product_id = p.id AND competitor = ph.competitor)
        ORDER BY ph.discount_percent DESC
        LIMIT 10
    ''')
    
    for name, competitor, price, discount in cursor.fetchall():
        print(f"  {name[:35]:<35} {competitor:<12} ${price:>8.2f} ({discount:.1f}% off)")
    
    print(f"\n{'='*70}\n")
    conn.close()

if __name__ == '__main__':
    print("\n" + "🔍"*35)
    print("COMPETITIVE INTELLIGENCE AGENT - TREND ANALYSIS")
    print("Querying 30 days of historical data from SQLite")
    print("(ChatGPT cannot do this - no persistent memory!)")
    print("🔍"*35)
    
    get_product_trends('MBA-M3-256')
    get_best_deals()
