# Potato-Trading-Bot

## Run the API (FastAPI + scheduler)

PowerShell:
```powershell
# from C:\Users\God\Documents\PotatoBot\Potato-Trading-Bot
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r trading-bot-backend\requirements.txt

# keep .env in repo root so python-dotenv can load it
uvicorn main:app --app-dir trading-bot-backend --reload
```

Endpoints:
- http://127.0.0.1:8000/
- http://127.0.0.1:8000/trade
- http://127.0.0.1:8000/trades
- http://127.0.0.1:8000/stats

## Run the backtest script

```powershell
python trading-bot-backend\backtesting\run_backtest.py
```
