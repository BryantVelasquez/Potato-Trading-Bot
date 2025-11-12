# utils/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from trading.paper_trader import PaperTrader
from strategies.sma_crossover import SMAStrategy

def start_scheduler(bot):
    print("[SCHEDULER] STARTING BACKGROUND TRADING....")
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: bot.execute_trade("BTC-USD"), "interval", minutes=1)
    scheduler.start()
    print("[SCHEDULER] JOB STARTED")

