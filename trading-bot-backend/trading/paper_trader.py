from datetime import datetime
from database.db import db
from colorama import Fore, Style
import yfinance as yf
class PaperTrader:
    def __init__(self, strategy, initial_balance=10000):
        self.strategy = strategy
        self.balance = initial_balance
        self.position = None  # holes {'symbol': str, 'price': float}
        self.trade_log = []
        self.trades_collection = db["trades"]

    def execute_trade(self, symbol: str):
        # Load only ONE dataset for both signal and price
        data = yf.download(symbol, period="3d", interval="5m", auto_adjust=False)
        if data.empty:
            print("[ERROR] NO DATA")
            return {"message": "No data returned"}

        signal = self.strategy.generate_signal(data)
        price = float(data["Close"].iloc[-1].item())

        # BUY LOGIC
        if signal == "BUY" and self.position is None:
            trade = {
                "symbol": symbol,
                "price": price,
                "timestamp": datetime.now(),
                "action": "BUY",
                "balance": self.balance
            }
            self.trades_collection.insert_one(trade)
            self.trade_log.append(trade)
            self.position = {"symbol": symbol, "price": price}

            print(Fore.GREEN + f"[SCHEDULER]: Bought {symbol} at {price}" + Style.RESET_ALL)
            return {"message": f"Bought {symbol} at {price}"}

        # SELL LOGIC
        elif signal == "SELL" and self.position:
            profit = price - self.position["price"]
            self.balance += profit
            trade = {
                "symbol": symbol,
                "price": price,
                "timestamp": datetime.now(),
                "action": "SELL",
                "balance": self.balance,
                "profit": profit
            }
            self.trades_collection.insert_one(trade)
            self.trade_log.append(trade)
            self.position = None
            print(Fore.RED + f"[SCHEDULER]: Sold {symbol} at {price}, Profit {profit:.2f}" + Style.RESET_ALL)
            return {"message": f"Sold {symbol} at {price}, Profit: {profit:.2f}"}
        
        print(Fore.YELLOW + f"NO TRADE EXECUTED FOR {symbol} ({signal})" + Style.RESET_ALL)
        return {"message": f"No trade executed for {symbol}({signal})."}

    def _get_latest_price(self, data):
        try:
            price = float(data["Close"].iloc[-1])
            return price
        except:
            print("[ERROR] NO LATEST PRICE FOUND")
            return None
 

