from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)
uri = "mongodb+srv://javierarroyosolis46:Lostmy-63313113@techiescluster.0zyk4.mongodb.net/?retryWrites=true&w=majority&appName=TechiesCluster"

client = MongoClient(uri)
db = client["techies_dbs"]

@app.route('/')
def home():
    try:
        return db.list_collection_names()
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
