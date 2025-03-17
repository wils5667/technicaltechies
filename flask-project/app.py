from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)
uri = "mongodb+srv://javierarroyosolis46:Lostmy-63313113@techiescluster.0zyk4.mongodb.net/?retryWrites=true&w=majority&appName=TechiesCluster"

client = MongoClient(uri)
db = client.get_database("techies_db")

@app.route('/')
def home():
    return "Hello, Techies!"
