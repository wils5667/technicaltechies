from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from bson.json_util import dumps
from datetime import datetime

# Initialize Flask app and MongoDB client
app = Flask(__name__)
uri = "mongodb+srv://javierarroyosolis46:Lostmy-63313113@techiescluster.0zyk4.mongodb.net/?retryWrites=true&w=majority&appName=TechiesCluster"

# Connect to MongoDB and the techies_dbs database
client = MongoClient(uri)
db = client["techies_dbs"]

# Function to retrieve all products from the products collection
def get_all_products():
    products = db["products"].find()
    products_list = []
    for product in products:
        expiry_date = product.get("expirationDate")
        if expiry_date and isinstance(expiry_date, datetime):
            expiry_date = expiry_date.strftime("%Y-%m-%d")
        product_data = {
            "id": str(product["_id"]),
            "name": product.get("productName"),
            "brand": product.get("brand"),
            "category": product.get("category"),
            "productID": product.get("productID"),
            "volume": product.get("volume"),
            "cost": product.get("costPrice"),
            "expiryDate": expiry_date,
            "reorder": product.get("reorderLevel"),
            "sales": product.get("salesCount"),
            "selling": product.get("sellingPrice"),
            "stock": product.get("stock"),
            "revenue": product.get("totalRevenue")
        }
        products_list.append(product_data)
    return products_list

# Function to retrieve all users from the users collection
def get_all_users():
    users = db["users"].find()
    users_list = []
    for user in users:
        user_data = {
            "id": str(user["_id"]),
            "accountID": user.get("accountID"),
            "password": user.get("password"),
            "email": user.get("email"),
            "number": user.get("phoneNumber")
        }
        users_list.append(user_data)
    return users_list

# Route for the home page
@app.route('/')
def home():
    return render_template('home.html', page_title="HOME", products=get_all_products())

# Route for the add new page
@app.route('/addnew', methods=['GET', 'POST'])
def addnew():
    if request.method == 'POST':
        # handle form submission
        return redirect(url_for('home'))
    return render_template('addnew.html', page_title="ADD NEW")

# Route for the edit page
@app.route('/edititem', methods=['GET', 'POST'])
def edititem():
    item_id = request.args.get('item_id')
    # process item_id
    return render_template('edititem.html', page_title="EDIT ITEM", product=product)
# Route for the search page
@app.route('/search')
def search():
    return render_template('search.html', page_title="SEARCH")

# Route for the lables page
@app.route('/lables')
def lables():
    return render_template('lables.html', page_title="LABLES")

# Route for the settings page
@app.route('/settings')
def settings():
    return render_template('settings.html', page_title="SETTINGS")

# Route for the print reports options page
@app.route('/printreports')
def printreports():
    return render_template('printreports.html', page_title="PRINT REPORTS")

if __name__ == '__main__':
    app.run(debug=False)
