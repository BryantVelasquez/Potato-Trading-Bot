import pandas as pd
import numpy as np

class SMAStrategy:
    def __init__(
            self, 
            short_window=9, 
            long_window=21, 
            trend_window=200
        ):
        self.trend_window = trend_window
        self.short_window = short_window
        self.long_window = long_window

    def generate_signal(self, data: pd.DataFrame):

        close = data["Close"]

        # Need enough data
        if len(data) < self.trend_window + 20:
            return "HOLD"

        high = data["High"]
        low = data["Low"]

        # SMA indicators
        sma_short = close.rolling(self.short_window).mean()
        sma_long = close.rolling(self.long_window).mean()
        sma_trend = close.rolling(self.trend_window).mean()

        # Atr Calculation
        tr1 = high - low
        tr2 = (high - close.shift(1)).abs()
        tr3 = (low - close.shift(1)).abs()
        true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

        atr = true_range.rolling(14).mean()

        # Current values
        price = close.iloc[-1]

        prev_short = sma_short.iloc[-2]
        curr_short = sma_short.iloc[-1]

        prev_long = sma_long.iloc[-2]
        curr_long = sma_long.iloc[-1]

        curr_trend = sma_trend.iloc[-1]

        curr_atr = atr.iloc[-1]
        atr_mean = atr.iloc[-20:].mean()

        # ATR volatility bands
        atr_low = 0.8 * atr_mean
        atr_high = 1.4 * atr_mean

        # Voltality Filter
        if not (atr_low < curr_atr < atr_high):
            return "HOLD"

        # Trend Filter
        if price < curr_trend:
            return "HOLD"

        # Crossover Logic
        buy_cross = prev_short < prev_long and curr_short > curr_long
        sell_cross = prev_short > prev_long and curr_short < curr_long

        # Slope filter
        long_slope = sma_long.iloc[-1] - sma_long.iloc[-3]

        if buy_cross and long_slope > 0:
            return "BUY"

        if sell_cross and long_slope < 0:
            return "SELL"

        return "HOLD"