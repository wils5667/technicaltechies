#Core flask and DB Imports
from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from bson.json_util import dumps
from datetime import datetime

#Login/authentication setup
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from dotenv import load_dotenv
import os
from flask import session
from .database import users_collection

#load .env
load_dotenv()
# Initialize Flask app and MongoDB client
app = Flask(__name__)

#secret keys
app.secret_key = os.getenv("SECRET_KEY")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


# Grab MongoDB URI
uri = os.getenv("MONGODB_URI")
client = MongoClient(uri)
db = client["techies_dbs"]
users_collection = db["users"]

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
    if "user" not in session:
        return redirect(url_for('login'))
    return render_template('home.html', page_title="HOME", products=get_all_products())

# Route for the add new page
@app.route('/addnew', methods=['GET', 'POST'])
def addnew():
    if request.method == 'POST':
        # Get form data given by the user
        name = request.form.get('item-name')
        brand = request.form.get('brand')
        category = request.form.get('category')
        serial = request.form.get('serial-number')
        volume = float(request.form.get('volume', 0))
        cost = float(request.form.get('cost-price', 0))
        selling = float(request.form.get('selling-price', 0))
        expiry = request.form.get('item-expiration')
        reorder = int(request.form.get('reorder-level', 0))
        sales = int(request.form.get('sales-count', 0))
        stock = int(request.form.get('stock', 0))
        revenue = float(request.form.get('total-revenue', 0))

        # Convert the expiry date to a datetime object if provided
        expiry_date = datetime.strptime(expiry, "%Y-%m-%d") if expiry else None

        # Create a new product dictionary to insert into the database
        new_product = {
            "productName": name,
            "brand": brand,
            "category": category,
            "productID": serial,
            "volume": volume,
            "costPrice": cost,
            "sellingPrice": selling,
            "expirationDate": expiry_date,
            "reorderLevel": reorder,
            "salesCount": sales,
            "stock": stock,
            "totalRevenue": revenue
        }

        # Insert the new product into the products collection
        db["products"].insert_one(new_product)

        # Handle form submission
        return redirect(url_for('home'))
    return render_template('addNew.html', page_title="ADD NEW")

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
    return render_template('lables.html', page_title="LABELS")

# Route for the settings page
@app.route('/settings')
def settings():
    return render_template('settings.html', page_title="SETTINGS")

# Route for the print reports options page
@app.route('/printreports')
def printreports():
    return render_template('printreports.html', page_title="PRINT REPORTS")

#Registration route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Prevent duplicate accounts
        if users_collection.find_one({"accountID": username}):
            return "Username already exists", 400

        hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")
        users_collection.insert_one({
            "accountID": username,
            "password": hashed_pw
        })

        return redirect(url_for("login"))
    return render_template("Createaccount.html")

#Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            username = request.form["username"]
            password = request.form["password"]
        except KeyError:
            return "Missing form fields", 400

        user = users_collection.find_one({"accountID": username})
        print("User from DB:", user) 

        if user and user["password"] == password:
            session["user"] = username
            return redirect(url_for("home"))

        return "Invalid credentials", 401
        
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)
