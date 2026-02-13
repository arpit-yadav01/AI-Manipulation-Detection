from pymongo import MongoClient
import os

# Mongo connection (Docker service name = mongo)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")

client = MongoClient(MONGO_URI)

# Database name
db = client["realitycheck"]

# Collection used everywhere
mongo = db
