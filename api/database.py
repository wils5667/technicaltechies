# api/database.py

import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv()

# Get MongoDB URI from .env
MONGO_URI = os.getenv("MONGODB_URI")

# Connect to MongoDB
client = MongoClient(MONGODB_URI)

# Use the actual database name: techies_dbs
db = client["techies_dbs"]

# Access the 'users' collection
users_collection = db["users"]
