from flask import Flask, render_template, redirect, url_for, session, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb+srv://JavierAAS46:Lostmy-63313113@techiescluster.0zyk4.mongodb.net/?retryWrites=true&w=majority&appName=TechiesCluster"

mongo = PyMongo(app)

@app.route("/")
def home():
    return "MongoDB connected successfully"

if __name__ == "__main__":
    app.run(debug=True)


@app.route("/products", methods=['GET'])
def get_products():
    products = mongo.db.products.find()
    product_list = [{
        "id": str(product["_id"]),
        "name": product["productName"],
        "brand": product["brand"],
        "catagory": product["catagory"],
        "productID": product["productID"],
        "volume": product["volume"]
    } for product in products]

    return jsonify(product_list)