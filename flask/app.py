from flask import Flask
from pymongo.mongo_client import MongoClient

app = Flask(__name__)

uri = "mongodb+srv://javierarroyosolis46:Lostmy-63313113@techiescluster.0zyk4.mongodb.net/?retryWrites=true&w=majority&appName=TechiesCluster"

client = MongoClient(uri)
db = client["techies_dbs"]

@app.route('/')
def home():
    try:
        client.admin.command('ping')
        return "Pinged your deployment. You successfully connected to MongoDB!"
    except Exception as e:
        return e
    
if __name__ == '__main__':
    app.run(debug=True)