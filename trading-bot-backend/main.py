# main.py
from fastapi import FastAPI
from trading.paper_trader import PaperTrader
from strategies.sma_crossover import SMAStrategy
from database.db import db
from utils.scheduler import start_scheduler
from bson import ObjectId

app = FastAPI(title="Trading Bot API")


strategy = SMAStrategy(short_window=5, long_window=20)
bot = PaperTrader(strategy=strategy)

@app.get("/")
def home():
    return {"message": "Trading bot is running!"}

@app.get("/trade")
def run_trade():
    result = bot.execute_trade("AAPL")
    return result

@app.get("/trades")
def get_trades():
    trades = list(db["trades"].find().sort("timestamp", -1))
    # Convert ObjectId to string for JSON serialization
    for trade in trades:
        trade["_id"] = str(trade["_id"])
    return {"count": len(trades), "trades": trades}

@app.get("/stats")
def get_stats():
    trades = list(db["trades"].find())
    if not trades:
        return {"message": "No trades yet."}

    total_profit = sum([t.get("profit", 0) or 0 for t in trades])
    wins = sum(1 for t in trades if t.get("profit", 0) > 0)
    total_trades = sum(1 for t in trades if t["action"] == "SELL")
    win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
    last_balance = trades[-1]["balance"] if trades else 0

    return {
        "total_trades": total_trades,
        "total_profit": round(total_profit, 2),
        "win_rate": round(win_rate, 2),
        "balance": round(last_balance, 2)
    }

# Background scheduler
start_scheduler(bot)
