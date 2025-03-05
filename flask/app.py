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
