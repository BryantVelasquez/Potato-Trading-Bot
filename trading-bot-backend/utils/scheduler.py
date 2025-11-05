# utils/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler

def start_scheduler(bot):
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: bot.execute_trade("AAPL"), "interval", minutes=10)
    scheduler.start()
