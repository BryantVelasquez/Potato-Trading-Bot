# Potato Trading Bot

## Overview

This project is a fully modular automated trading bot built in Python. It supports paper trading, strategy execution, backtesting, scheduled trading jobs, and MongoDB-based storage for trades and portfolio data. The system is designed so new strategies can be added easily and evaluated against historical data.

---

## Features

* **Paper Trading Engine** with risk controls, slippage, and fees
* **Backtesting Framework** for multi-year performance testing
* **Strategy Layer** (currently SMA Crossover, expandable to others)
* **MongoDB Integration** for trades, logs, and account history
* **Background Scheduler** to automate trades at intervals

---

## Project Structure

```
POTATO-TRADING-BOT/
└── trading-bot-backend/
    ├── backtesting/
    │   └── run_backtest.py        # Entry point for backtesting runs
    │
    ├── database/
    │   ├── db.py                  # MongoDB connection setup
    │   └── models.py              # Database models & helper functions
    │
    ├── strategies/
    │   └── sma_crossover.py       # SMA strategy implementation
    │
    ├── trading/
    │   ├── Backtester.py          # Backtesting engine class
    │   ├── logger.py              # Logging utilities
    │   └── paper_trader.py        # Paper trading engine
    │
    ├── utils/
    │   └── scheduler.py           # APScheduler background jobs
    │
    ├── main.py                    # Application entry point
    ├── requirements.txt           # Python dependencies
    ├── .env                       # Environment variables
    └── .gitignore
```

---

## Folder & File Descriptions

### **backtesting/**

#### `run_backtest.py`

Runs a full backtest using historical asset data. Allows selecting strategy, timeframe, and initial balance.

### **database/**

#### `db.py`

Creates and manages MongoDB client/connection.

#### `models.py`

Defines helper functions for inserting trades, logs, balance updates, etc.

### **strategies/**

#### `sma_crossover.py`

Contains the SMA crossover strategy logic. Returns BUY/SELL/HOLD based on moving average relationships.

### **trading/**

#### `Backtester.py`

Handles historical evaluation of any strategy passed to it. Tracks balance, P/L, trade count, and more.

#### `logger.py`

Simple logging abstraction for file/db logs.

#### `paper_trader.py`

Executes virtual trades with:

* Risk per trade (% account)
* Fee rate
* Slippage
* Position sizing

### **utils/**

#### `scheduler.py`

Runs automated trading jobs using APScheduler. Fetches live data, executes strategy, and logs trades.

### **main.py`

Backend startup file. Loads environment variables, connects to DB, starts scheduler, and can expose routes (if chosen).

---

## How It Works

### **Strategy Execution**

1. Live or historical data is retrieved (`yfinance`).
2. Strategy calculates indicators (ex: SMAs).
3. A signal is returned.

### **Paper Trading Engine**

1. Determines position size based on account risk percentage.
2. Executes trade with fee & slippage applied.
3. Logs trade to MongoDB.

### **Backtesting Engine**

1. Processes years of data bar-by-bar.
2. Simulates trades using the strategy.
3. Tracks and reports:

   * Total return
   * Max drawdown
   * Win/loss ratio
   * Number
