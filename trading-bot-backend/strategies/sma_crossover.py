import yfinance as yf
import pandas as pd

class SMAStrategy:
    def __init__(self, short_window=5, long_window=20):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signal(self, symbol: str):
        data = yf.download(symbol, period="1mo", interval="1h")
        data["SMA_short"] = data["Close"].rolling(window=self.short_window).mean()
        data["SMA_long"] = data["Close"].rolling(window=self.long_window).mean()

        if data["SMA_short"].iloc[-1] > data["SMA_long"].iloc[-1]:
            return "BUY"
        elif data["SMA_short"].iloc[-1] < data["SMA_long"].iloc[-1]:
            return "SELL"
        else:
            return "HOLD"
