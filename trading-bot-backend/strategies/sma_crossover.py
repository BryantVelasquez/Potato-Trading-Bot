import yfinance as yf
import pandas as pd
import random
class SMAStrategy:
    def __init__(self, short_window=3, long_window=5):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signal(self, symbol: str):
        
        data = yf.download(symbol, period="1d", interval="5m", auto_adjust= False)
        data["SMA_short"] = data["Close"].rolling(window=self.short_window).mean()
        data["SMA_long"] = data["Close"].rolling(window=self.long_window).mean()

        if len(data) < 2:
            print(f"[WARN] NOT ENOUGH ROWS TO COMPARE SMA CROSSOVER FOR {symbol}")
            return None

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
