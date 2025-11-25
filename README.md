# Competitive Intelligence Agent (MCP-Powered)

This system demonstrates capabilities that ChatGPT simply cannot replicate - persistent data storage, automated monitoring, and version-controlled reporting.


This system uses **6 MCP servers** working together:

| Server | Purpose | ChatGPT Alternative |
|--------|---------|--------------------|
| **SQLite** | Store 30+ days of price history | ❌ None - forgets between sessions |
| **Firecrawl** | Structured web scraping with schemas | ⚠️ Basic browsing, unreliable |
| **Node.js** | Statistical calculations, charts | ⚠️ Code interpreter (limited) |
| **GitHub** | Version-controlled reports | ❌ Manual copy-paste only |
| **Context7** | Up-to-date library documentation | ❌ Training cutoff issues |
| **Sequential Thinking** | Complex multi-factor decisions | ⚠️ Basic reasoning |

## 📊 Demo Results

This demo created:
- **1,200 price records** across 8 products, 5 competitors, 30 days
- **39 price alerts** triggered automatically when prices dropped >5%
- **Trend analysis** showing 10-36% discounts from MSRP
- **Persistent database** that survives between conversations

## 🏗️ Architecture

```
+---------------------------------------------------------------------+
|                        USER REQUEST                                  |
|            "Monitor MacBook Air M3 prices"                          |
+-----------------------------+---------------------------------------+
                              |
                              v
+---------------------------------------------------------------------+
|                     AI + MCP GATEWAY                                |
|              Orchestrates tools based on intent                     |
+-----------------------------+---------------------------------------+
                              |
        +---------------------+---------------------+
        |                     |                     |
        v                     v                     v
+---------------+    +---------------+    +---------------+
|   FIRECRAWL   |    |    SQLITE     |    |    GITHUB     |
|  Scrape Web   |    |  Store Data   |    |  Push Reports |
+---------------+    +---------------+    +---------------+
        |                     |                     |
        +---------------------+---------------------+
                              |
                              v
+---------------------------------------------------------------------+
|               SEQUENTIAL THINKING + CONTEXT7                        |
|           Complex reasoning + Documentation lookup                  |
+---------------------------------------------------------------------+
```

## 🚀 Quick Start

### 1. Initialize Database
```bash
python3 scripts/init_database.py
```

### 2. Run Trend Analysis
```bash
python3 scripts/analyze_trends.py
```

### 3. View Dashboard
Open `dashboard/competitive-intelligence-dashboard.html` in your browser.

## 📁 Project Structure

```
├── scripts/
│   ├── init_database.py      # Create SQLite DB with sample data
│   └── analyze_trends.py     # Query historical trends
├── dashboard/
│   └── competitive-intelligence-dashboard.html
├── reports/
│   └── 2025-11-24-weekly-report.md
└── README.md
```

## 💡 Key Insights from Demo

### Best Deals Found (from 30-day analysis)
| Product | Retailer | Price | Discount |
|---------|----------|-------|----------|
| MacBook Air M3 256GB | Best Buy | $700.16 | 36.3% off |
| Xbox Series X | Walmart | $347.16 | 30.4% off |
| AirPods Pro 2nd Gen | Walmart | $177.12 | 28.9% off |
| MacBook Air M3 512GB | Costco | $930.99 | 28.3% off |
| Nintendo Switch OLED | Costco | $254.14 | 27.2% off |

### 30-Day Price Movement
- **Best Buy**: -32.4% (most aggressive pricing)
- **Costco**: -29.6% 
- **Walmart**: -21.1%
- **Amazon**: -11.4%
- **Target**: -10.5%


### Prompt: "What happened to MacBook prices last week?"

**ChatGPT Response**:
> "I don't have access to real-time data or your previous conversations. You would need to provide me with the price information."

**MCP Agent Response**:
```sql
SELECT competitor, price, scraped_at 
FROM price_history 
WHERE product_id = 1 AND scraped_at > date('now', '-7 days')
ORDER BY scraped_at;
```
→ Returns 35 data points instantly from persistent storage.

