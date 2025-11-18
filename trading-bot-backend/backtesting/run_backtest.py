import sys
import os
import yfinance as yf
# Make project root importable (so Backtester + strategy load correctly)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from trading.Backtester import Backtester
from strategies.sma_crossover import SMAStrategy



# Load historical data (Yahoo max for 1h interval = 2 yrs)
print("[INFO] Downloading historical data...")

data = yf.download("NQ=F", period="1y", interval="1h")

if data is None or data.empty:
    raise ValueError("No historical data returned from Yahoo Finance.")



# Backtest Setup
strategy = SMAStrategy(short_window=21, long_window=100)
backtester = Backtester(strategy=strategy, initial_balance=10000)

# Run Backtest
print("[INFO] Running backtest...")

results = backtester.run_backtest(data)

print("\n========== BACKTEST RESULTS ==========")
print(f"Initial Balance:  ${results['initial_balance']}")
print(f"Final Balance:    ${results['final_balance']}")
print(f"Total Profit:     ${results['total_profit']}")
print(f"Return:           {results['return_%']}%")
print(f"Total Trades:     {results['total_trades']}\n")

print("Trade History:")
for t in results["trade_history"]:
    print(t)

print("======================================\n")
