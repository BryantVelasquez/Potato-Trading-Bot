from datetime import datetime
from database.db import db
from colorama import Fore, Style
class PaperTrader:
    def __init__(self, strategy, initial_balance=10000):
        self.strategy = strategy
        self.balance = initial_balance
        self.position = None  # holes {'symbol': str, 'price': float}
        self.trade_log = []
        self.trades_collection = db["trades"]

    def execute_trade(self, symbol: str):
        signal = self.strategy.generate_signal(symbol)
        price = self._get_latest_price(symbol)

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

    def _get_latest_price(self, symbol):
        import yfinance as yf
        try:
            data = yf.download(symbol, period="3d", interval="1h", auto_adjust= False)
            if data.empty:
                print(f"[ERROR] No data returned for {symbol}")
                return None
            return float(data["Close"].iloc[-1].item())
        except Exception as e:
            print(f"[ERROR] FAILED TO FETCH PRICE FOR {symbol}: {e}")
            return None
 

