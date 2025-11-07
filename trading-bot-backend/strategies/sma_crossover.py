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

        #Use to compare prev short/long and curr short/long
        prev_short = data["SMA_short"].iloc[-2]
        curr_short = data["SMA_short"].iloc[-1]
        prev_long = data["SMA_long"].iloc[-2]
        curr_long = data["SMA_long"].iloc[-1]


        if prev_short < prev_long and curr_short > curr_long:
            return "BUY" # short SMA crossed above long SMA
        elif prev_short > prev_long and curr_short < curr_long :
            return "SELL" # short SMA below long SMA
        else:
            return "HOLD"
