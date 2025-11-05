from fastapi import FastAPI
from trading.paper_trader import PaperTrader
from strategies.sma_crossover import SMAStrategy
from utils.scheduler import start_scheduler

app = FastAPI(title="Trading Bot API")

# Initialize bot components
strategy = SMAStrategy(short_window=5, long_window=20)
bot = PaperTrader(strategy=strategy)

@app.get("/")
def home():
    return {"message": "Trading bot is running!"}

@app.get("/trade")
def run_trade():
    """Trigger a single trade manually (for testing)."""
    result = bot.execute_trade("AAPL")  # Example stock
    return result

# Background scheduler to automate trading every X minutes
start_scheduler(bot)
