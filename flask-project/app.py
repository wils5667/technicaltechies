from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from bson.json_util import dumps

app = Flask(__name__)
uri = "mongodb+srv://javierarroyosolis46:Lostmy-63313113@techiescluster.0zyk4.mongodb.net/?retryWrites=true&w=majority&appName=TechiesCluster"

client = MongoClient(uri)
db = client["techies_dbs"]

@app.route('/')
def home():
    try:
        products = list(db["products"].find())
        products_html = "<br>".join([dumps(product) for product in products])
        return products_html
    except Exception as e:
        return str(e)
    #return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
