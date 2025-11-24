# 🧪 Testing Guide

This guide walks you through testing the Competitive Intelligence Agent locally.

## Prerequisites

- **Python 3.8+** (for SQLite scripts)
- **Web Browser** (for dashboard)
- **Git** (to clone the repo)

## Quick Start (5 Minutes)

### Step 1: Clone the Repository

```bash
git clone https://github.com/ajeetraina/competitive-intelligence-agent-mcp.git
cd competitive-intelligence-agent-mcp
```

### Step 2: Create Data Directory

```bash
mkdir -p data
```

### Step 3: Initialize the Database

```bash
python3 scripts/init_database.py
```

**Expected Output:**
```
🚀 Competitive Intelligence Agent - Database Initialization
============================================================
WHY MCP MATTERS: This data PERSISTS between conversations!
ChatGPT would forget all this the moment you close the tab.
============================================================

✅ Database schema created successfully!

📦 Populating 30 days of price history for 8 products...
✅ Inserted 1,200 price records
🚨 Generated ~40 price alerts

============================================================
📊 DATABASE STATISTICS
============================================================
Products tracked: 8
Price history records: 1,200
Date range: [30 days ago] to [today]
Competitors: Amazon, Best Buy, Costco, Target, Walmart
Unacknowledged alerts: ~40
============================================================

✅ Database ready at: data/price_intelligence.db
🔑 This database will persist for future queries!
```

### Step 4: Run Trend Analysis

```bash
python3 scripts/analyze_trends.py
```

**Expected Output:**
```
🔍 COMPETITIVE INTELLIGENCE AGENT - TREND ANALYSIS
Querying 30 days of historical data from SQLite

======================================================================
📊 PRICE TREND ANALYSIS: MacBook Air M3 256GB
======================================================================
Brand: Apple | Category: Laptops | MSRP: $1099.0

💰 CURRENT PRICES
--------------------------------------------------
  Best Buy     $700.16  (36.3% off)  ✅ In Stock 🏆 BEST
  Costco       $843.34  (23.3% off)  ✅ In Stock
  Walmart      $805.21  (26.7% off)  ✅ In Stock
  ...

🏆 BEST DEALS ACROSS ALL PRODUCTS
--------------------------------------------------
  MacBook Air M3 256GB    Best Buy    $700.16   36.3% off
  Xbox Series X           Walmart     $347.16   30.4% off
  ...
```

### Step 5: View the Dashboard

```bash
# Option 1: Open directly in browser
open dashboard/competitive-intelligence-dashboard.html

# Option 2: Use Python's built-in server
cd dashboard
python3 -m http.server 8080
# Then visit: http://localhost:8080/competitive-intelligence-dashboard.html
```

---

## 🔬 Advanced Testing

### Test 1: Query the Database Directly

```bash
# Open SQLite CLI
sqlite3 data/price_intelligence.db

# List all products
SELECT * FROM products;

# Get latest prices for MacBook Air M3
SELECT competitor, price, discount_percent, scraped_at 
FROM price_history 
WHERE product_id = 1 
ORDER BY scraped_at DESC 
LIMIT 10;

# Find all price alerts
SELECT p.name, pa.competitor, pa.old_price, pa.new_price, pa.change_percent
FROM price_alerts pa
JOIN products p ON pa.product_id = p.id
ORDER BY pa.change_percent ASC
LIMIT 10;

# Exit SQLite
.quit
```

### Test 2: Verify Data Persistence

This is the **key MCP differentiator** - data survives between sessions!

```bash
# Run analysis
python3 scripts/analyze_trends.py

# Close terminal, wait a few minutes, open new terminal

# Run analysis again - same data is there!
python3 scripts/analyze_trends.py
```

**ChatGPT cannot do this** - it forgets everything between conversations.

### Test 3: Check Alert Thresholds

```bash
sqlite3 data/price_intelligence.db "SELECT COUNT(*) FROM price_alerts WHERE change_percent < -5;"
```

This shows how many times prices dropped more than 5% - triggering automatic alerts.

### Test 4: Verify Database Schema

```bash
sqlite3 data/price_intelligence.db ".schema"
```

**Expected Output:**
```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sku TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    category TEXT,
    brand TEXT,
    msrp REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE price_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    competitor TEXT NOT NULL,
    price REAL NOT NULL,
    ...
);

CREATE TABLE price_alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    alert_type TEXT NOT NULL,
    ...
);
```

---

## 🐳 Docker Testing (Optional)

If you prefer Docker:

```bash
# Build image
docker build -t competitive-intel-agent .

# Run container
docker run -it --rm -v $(pwd)/data:/app/data competitive-intel-agent

# Inside container
python3 scripts/init_database.py
python3 scripts/analyze_trends.py
```

---

## ✅ Test Checklist

| Test | Command | Expected Result |
|------|---------|-----------------|
| Database creation | `python3 scripts/init_database.py` | 1,200 records created |
| Trend analysis | `python3 scripts/analyze_trends.py` | Price trends displayed |
| Dashboard loads | Open HTML in browser | Charts render correctly |
| Data persists | Run analysis twice | Same data both times |
| Alerts generated | Check `price_alerts` table | ~40 alerts with >5% drops |

---

## 🐛 Troubleshooting

### "No module named sqlite3"
```bash
# SQLite is built into Python, but if missing:
pip install pysqlite3
```

### "Database not found"
```bash
# Make sure you're in the repo root
cd competitive-intelligence-agent-mcp
mkdir -p data
python3 scripts/init_database.py
```

### "Permission denied"
```bash
chmod +x scripts/*.py
```

### Dashboard charts not loading
- Make sure you have internet connection (Chart.js loads from CDN)
- Try opening in Chrome/Firefox instead of Safari

---

## 📊 Sample Queries to Try

```sql
-- Best deal right now
SELECT p.name, ph.competitor, ph.price, ph.discount_percent
FROM products p
JOIN price_history ph ON p.id = ph.product_id
WHERE ph.scraped_at = (SELECT MAX(scraped_at) FROM price_history)
ORDER BY ph.discount_percent DESC
LIMIT 1;

-- Price volatility by retailer
SELECT competitor, 
       AVG(price) as avg_price,
       MIN(price) as min_price,
       MAX(price) as max_price,
       (MAX(price) - MIN(price)) / AVG(price) * 100 as volatility_pct
FROM price_history
WHERE product_id = 1
GROUP BY competitor
ORDER BY volatility_pct DESC;

-- Products with most alerts
SELECT p.name, COUNT(*) as alert_count
FROM price_alerts pa
JOIN products p ON pa.product_id = p.id
GROUP BY p.id
ORDER BY alert_count DESC;
```

---

## 🎯 The MCP Proof Point

After running these tests, you've demonstrated that:

1. ✅ **Data persists** in SQLite between sessions
2. ✅ **Alerts auto-generate** without human prompting
3. ✅ **Historical queries** work instantly on 30 days of data
4. ✅ **Reports are versioned** in GitHub

**This is what ChatGPT cannot do!**

---

## 📚 Next Steps

1. Modify `scripts/init_database.py` to add your own products
2. Connect real Firecrawl scraping for live prices
3. Set up a cron job for automated daily updates
4. Build Slack/email notifications for alerts

---

*Questions? Open an issue on the repo!*
