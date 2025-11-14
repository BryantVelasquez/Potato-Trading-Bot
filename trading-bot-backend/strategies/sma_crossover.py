import yfinance as yf
import pandas as pd
import random
class SMAStrategy:
    def __init__(self, short_window=9, long_window=21):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signal(self, data: pd.DataFrame):
        #Calculate indicators
        data["SMA_short"] = data["Close"].rolling(self.short_window).mean()
        data["SMA_long"] = data["Close"].rolling(self.long_window).mean()
        
        # Need at least 2 rows to compare
        if len(data) < 2:
            return None

        #Use to compare prev short/long and curr short/long
        prev_short = data["SMA_short"].iloc[-2]
        curr_short = data["SMA_short"].iloc[-1]
        prev_long = data["SMA_long"].iloc[-2]
        curr_long = data["SMA_long"].iloc[-1]

        #Buy crossover
        if prev_short < prev_long and curr_short > curr_long:
            return "BUY" # short SMA crossed above long SMA
        #Sell crossover
        elif prev_short > prev_long and curr_short < curr_long :
            return "SELL" # short SMA below long SMA
        else:
            return "HOLD" 
