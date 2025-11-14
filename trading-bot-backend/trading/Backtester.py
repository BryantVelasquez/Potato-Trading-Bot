import pandas as pd
import warnings

# Suppress noisy Pandas warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)


class Backtester:
    def __init__(
        self, 
        strategy, 
        initial_balance,
        fee_rate=0.0005,        # 0.05% fee (binance)
        slippage_rate=0.0002,   # 0.02% slippage
        risk_per_trade=1.0      # % of account to use per trade (1.0 = 1%)
    ):
        self.strategy = strategy
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.position = None
        self.trade_history = []
        self.equity_curve = []

        self.fee_rate = fee_rate
        self.slippage_rate = slippage_rate
        self.risk_per_trade = risk_per_trade  # percent

    def run_backtest(self, data: pd.DataFrame):

        # Ensure data is sorted by datetime
        data = data.sort_index()

        # Flatten Yahoo Finance MultiIndex columns
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = [col[0] for col in data.columns]

        for i in range(len(data)):

            chunk = data.iloc[: i + 1].copy()
            signal = self.strategy.generate_signal(chunk)
            curr_price = chunk["Close"].iloc[-1].item()

            # --- Update equity curve (unrealized P/L)
            if self.position is not None:
                unrealized = (curr_price - self.position["entry_price"]) * self.position["quantity"]
                self.equity_curve.append(self.balance + unrealized)
            else:
                self.equity_curve.append(self.balance)

            # BUY
            
            if signal == "BUY" and self.position is None:

                # convert % to usable fraction
                capital_to_use = self.balance * (self.risk_per_trade / 100)

                if capital_to_use <= 0:
                    continue

                execution_price = self._apply_costs(curr_price)

                quantity = capital_to_use / execution_price

                self.position = {
                    "entry_price": execution_price,
                    "quantity": quantity
                }

                self.balance -= capital_to_use

                self.trade_history.append((
                    "BUY",
                    execution_price,
                    quantity
                ))

            
            # SELL
            
            elif signal == "SELL" and self.position is not None:

                execution_price = self._apply_costs_sell(curr_price)

                quantity = self.position["quantity"]
                entry_price = self.position["entry_price"]

                sell_value = execution_price * quantity
                entry_cost = entry_price * quantity

                profit = sell_value - entry_cost
                self.balance += sell_value

                self.trade_history.append((
                    "SELL",
                    execution_price,
                    quantity,
                    profit
                ))

                self.position = None

        #   Close position at end of backtest

        if self.position is not None:

            final_price = data["Close"].iloc[-1].item()
            execution_price = self._apply_costs_sell(final_price)

            quantity = self.position["quantity"]
            entry_price = self.position["entry_price"]

            sell_value = execution_price * quantity
            entry_cost = entry_price * quantity

            profit = sell_value - entry_cost
            self.balance += sell_value

            self.trade_history.append((
                "SELL_END",
                execution_price,
                quantity,
                profit
            ))

            self.position = None

        # return final stats
        return {
            "initial_balance": self.initial_balance,
            "final_balance": round(self.balance, 2),
            "total_profit": round(self.balance - self.initial_balance, 2),
            "return_%": round(((self.balance / self.initial_balance) - 1) * 100, 2),
            "total_trades": len([t for t in self.trade_history if "SELL" in t[0]]),
            "trade_history": self.trade_history,
        }

    
    def _apply_costs(self, price):
        """Applies fees and slippage to BUY price."""
        price_with_slippage = price * (1 + self.slippage_rate)
        total_cost = price_with_slippage * (1 + self.fee_rate)
        return total_cost

    def _apply_costs_sell(self, price):
        """Applies fees and slippage to SELL price."""
        price_with_slippage = price * (1 - self.slippage_rate)
        total_return = price_with_slippage * (1 - self.fee_rate)
        return total_return
