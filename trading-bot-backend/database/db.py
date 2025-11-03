from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")  # default local

client = MongoClient(MONGO_URI)
db = client["trading_bot"]

print("Successfully Connected to MongoDB")
