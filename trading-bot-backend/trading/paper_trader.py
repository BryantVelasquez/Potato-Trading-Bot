# trading/paper_trader.py
from datetime import datetime

class PaperTrader:
    def __init__(self, strategy, initial_balance=10000):
        self.strategy = strategy
        self.balance = initial_balance
        self.position = None  # e.g. "AAPL" or None
        self.trade_log = []

    def execute_trade(self, symbol: str):
        signal = self.strategy.generate_signal(symbol)
        price = self._get_latest_price(symbol)

        if signal == "BUY" and self.position is None:
            self.position = {"symbol": symbol, "price": price}
            self.trade_log.append({"action": "BUY", "symbol": symbol, "price": price, "time": datetime.now()})
            return {"message": f"Bought {symbol} at {price}"}

        elif signal == "SELL" and self.position:
            profit = price - self.position["price"]
            self.balance += profit
            self.trade_log.append({"action": "SELL", "symbol": symbol, "price": price, "profit": profit, "time": datetime.now()})
            self.position = None
            return {"message": f"Sold {symbol} at {price}, Profit: {profit:.2f}"}

        return {"message": f"No trade executed ({signal})."}

    def _get_latest_price(self, symbol):
        import yfinance as yf
        data = yf.download(symbol, period="1d", interval="1m")
        return data["Close"].iloc[-1]
