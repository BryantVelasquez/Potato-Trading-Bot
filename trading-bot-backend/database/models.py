from datetime import datetime

class TradeModel:
    def __init__(self, trade_id: str, symbol: str, quantity: float, price: float, trade_type: str, timestamp: datetime):
        self.trade_id = trade_id
        self.symbol = symbol
        self.quantity = quantity
        self.price = price
        self.trade_type = trade_type  # 'buy' or 'sell'
        self.timestamp = timestamp

    def to_dict(self):
        return {
            "trade_id": self.trade_id,
            "symbol": self.symbol,
            "quantity": self.quantity,
            "price": self.price,
            "trade_type": self.trade_type,
            "timestamp": self.timestamp.isoformat()
        }