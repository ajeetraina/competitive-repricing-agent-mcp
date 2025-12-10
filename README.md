# Competitive Repricing Agent (MCP-Powered)

An AI-powered competitive repricing system that monitors competitor prices and automatically adjusts your Stripe product prices to stay competitive. Built with **ChatGPT + Docker MCP Toolkit**.

## 🎯 What This Does

This agent demonstrates capabilities that ChatGPT alone cannot replicate:

- **Monitors competitor prices** in real-time (Amazon, Best Buy, Walmart)
- **Automatically reprices** your Stripe products to beat competitors
- **Logs all decisions** to SQLite for audit trail
- **Pushes reports** to GitHub for compliance

## 🔧 MCP Servers Used

| Server | Purpose |
|--------|--------|
| **Firecrawl** | Scrape competitor prices from retail websites |
| **Stripe** | Update your product prices automatically |
| **SQLite** | Store pricing history and audit logs |
| **GitHub** | Push repricing reports for compliance |
| **Sequential Thinking** | Complex pricing strategy decisions |
| **Context7** | Up-to-date library documentation |
| **Node.js Sandbox** | Statistical calculations |

## 📊 Latest Demo Results

**Date:** December 9, 2025  
**Product:** MacBook Air M3 13-inch 256GB

### Repricing Action Taken

| Metric | Before | After |
|--------|--------|-------|
| Your Price | $549.99 | $504.99 |
| Price Change | — | -$45.00 (-8.2%) |
| Market Position | 3rd | **#1 LOWEST** |

### Competitor Landscape

| Retailer | Price | vs. Our Price |
|----------|-------|---------------|
| **Our Store** | $504.99 | ✅ MARKET LEADER |
| Best Buy | $509.99 | +$5.00 (we beat by 1%) |
| Walmart | $669.00 | +$164.01 higher |
| Amazon | $699.00 | +$194.01 higher |

### Strategy Applied: UNDERCUT

- **Trigger:** Best Buy dropped to $509.99 (below our $549.99)
- **Calculation:** $509.99 × 0.99 = $504.99
- **Result:** We now have the lowest price by 1%

## 🏗️ Architecture

```
User: "Monitor MacBook Air M3 prices and stay competitive"
     │
     ▼
┌────────────────────────────────────────────────────────────────┐
│                   ChatGPT repricing. I need to:                │
│   1. Scrape competitor prices (Firecrawl MCP)                  │
│   2. Store in database (SQLite MCP)                            │
│   3. Compare & decide strategy (Sequential Thinking MCP)       │
│   4. Update price (Stripe MCP)                                 │
│   5. Push audit report (GitHub MCP)"                           │
└────────────────────────────────────────────────────────────────┘
     │                                                      ▲
     ▼                                                      │
┌─────────────────────┐                                     │
│     MCP Servers     │                                     │
│                     │                                     │
│  • Firecrawl MCP ───┼──► Scrapes Amazon, Best Buy,        │
│                     │    Walmart prices                   │
│                     │                                     │
│  • SQLite MCP ──────┼──► Stores price_history,            │
│                     │    repricing_log                    │
│                     │                                     │
│  • Stripe MCP ──────┼──► Creates new price,               │
│                     │    updates product                  │
│                     │                                     │
│  • GitHub MCP ──────┼──► Pushes audit report,             │
│                     │    commit SHA tracking              │
│                     │                                     │
│  • Sequential ──────┼──► Analyzes pricing strategy,       │
│    Thinking MCP     │    makes reprice decision           │
│                     │                                     │
│  • Node.js MCP ─────┼──► Calculates margins,              │
│                     │    statistics, charts               │
│                     │                                     │
│  • Context7 MCP ────┼──► API docs, library                │
│                     │    references                       │
└─────────────────────┘                                     │
     │                                                      │
     ▼                                                      │
┌────────────────────────────────────────────────────────────┐
│                      RESULT                                │
│  ✅ Price updated: $549.99 → $504.99                       │
│  ✅ SQLite logged: repricing_log entry #1                  │
│  ✅ GitHub pushed: commit 64a488aa                         │
│  ✅ Market position: #1 LOWEST PRICE                       │
└────────────────────────────────────────────────────────────┘
```

```
┌─────────────────────────────────────────────────────────────┐
│                     USER REQUEST                            │
│        "Monitor MacBook Air M3 and stay competitive"        │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              ChatGPT + MCP Gateway                          │
│           Orchestrates tools based on intent                │
└─────────────────────────┬───────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│   FIRECRAWL   │ │    STRIPE     │ │    SQLITE     │
│ Scrape Prices │ │ Update Price  │ │  Log Decision │
└───────────────┘ └───────────────┘ └───────────────┘
        │                 │                 │
        └─────────────────┼─────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                        GITHUB                                │
│              Push repricing report for audit                │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
├── reports/
│   └── repricing/
│       └── 2025-12-09-macbook-air-m3-repricing.md   # Latest repricing report
└── README.md
```

## 🚀 How to Use

1. **Set up Docker MCP Toolkit** with Firecrawl, Stripe, SQLite, GitHub servers
2. **Connect ChatGPT** to your MCP Gateway
3. **Use this prompt:**

```
Set up a competitive repricing agent:
1. I sell MacBook Air M3 on my store - current Stripe price is $549.99
2. Monitor competitor prices on Amazon, Walmart, Best Buy
3. When ANY competitor drops below my price:
   - Automatically update my Stripe product price to match or beat them
   - Use "undercut" strategy (price 1% below lowest competitor)
   - Log the repricing decision to SQLite
   - Push pricing change report to GitHub

Start monitoring now.
```

## 🔗 Related

- [Docker MCP Toolkit Documentation](https://docs.docker.com/mcp/)
- [Blog Post: How to Add MCP Servers to ChatGPT](https://docker.com/blog/add-mcp-server-to-chatgpt/)

---

*Powered by ChatGPT + Docker MCP Toolkit*
