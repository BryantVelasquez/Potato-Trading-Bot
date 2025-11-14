import pandas as pd
import numpy as np
import warnings

# Suppress noisy Pandas warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)


class Backtester:
    def __init__(self, strategy, initial_balance=10000):
        self.strategy = strategy
        self.initial_balance = initial_balance
        self.balance = initial_balance #updates with trades
        self.position = None #None when not holding // Number price was bought at
        self.trade_history = [] 
        self.equity_curve = []#Tracks account value every candle

    def run_backtest(self, data: pd.DataFrame):
        """
        Runs a simple SMA-crossover backtest using the SAME strategy logic
        used for live trading. Processes data candle-by-candle.
        """

        # Ensure datetime order
        data = data.sort_index()

        # FIX: Flatten MultiIndex columns if Yahoo Finance returns them
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = [col[0] for col in data.columns]

        for i in range(len(data)):
            # Use chunk up to current point
            chunk = data.iloc[: i + 1].copy()

            signal = self.strategy.generate_signal(chunk)

            # FIX: gives you most recent candle price with no warnings
            curr_price = chunk["Close"].iloc[-1].item()

            # Track P/L for charts/metrics
            if self.position is not None:
                unrealized = curr_price - self.position
                self.equity_curve.append(self.balance + unrealized)
            else:
                self.equity_curve.append(self.balance)


            # TRADE EXECUTION

            # BUY
            if signal == "BUY" and self.position is None:
                self.position = curr_price
                self.trade_history.append(("BUY", curr_price))

            # SELL
            elif signal == "SELL" and self.position is not None:
                profit = curr_price - self.position
                self.balance += profit
                self.trade_history.append(("SELL", curr_price, profit))
                self.position = None

        # When backtest ends stop holding and sell at last price
        if self.position is not None:
            final_price = data["Close"].iloc[-1].item()
            profit = final_price - self.position
            self.balance += profit
            self.trade_history.append(("SELL_END", final_price, profit))
            self.position = None

        # Final summary
        return {
            "initial_balance": self.initial_balance,
            "final_balance": round(self.balance, 2),
            "total_profit": round(self.balance - self.initial_balance, 2),
            "return_%": round(((self.balance / self.initial_balance) - 1) * 100, 2),
            "total_trades": len([t for t in self.trade_history if "SELL" in t[0]]),
            "trade_history": self.trade_history,
        }
