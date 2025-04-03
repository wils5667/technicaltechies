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
        product = {
            "item-name": request.form.get("item-name"),
            "brand": request.form.get("brand"),
            "category": request.form.get("category"),
            "serial-number": request.form.get("serial-number"),
            "volume": float(request.form.get("volume")),
            "cost-price": float(request.form.get("cost-price")),
            "selling-price": float(request.form.get("selling-price")),
            "stock": int(request.form.get("stock")),
            "item-expiration": datetime.strptime(request.form.get("item-expiration"), "%Y-%m-%d"),
            "reorder-level": int(request.form.get("reorder-level")),
            "sales-count": int(request.form.get("sales-count")),
            "total-revenue": float(request.form.get("total-revenue")),
        }

        # send to mongo
        db["products"].insert_one(product)

        # go back to home page
        return redirect('Home.html')
    return render_template('addnew.html', page_title="ADD NEW")

# Route for the edit page
@app.route('/edititem', methods=['GET', 'POST'])
def edititem():
    #item_id = request.args.get('serial-number')
    #if not item_id:
    #    return "Missing item ID", 400

    if request.method == 'POST':
        try:
            updated_data = {
                "item-name": request.form.get("item-name"),
                "brand": request.form.get("brand"),
                "category": request.form.get("category"),
                "serial-number": request.form.get("serial-number"),
                "volume": float(request.form.get("volume", "0")),
                "cost-price": float(request.form.get("cost-price", "0")),
                "selling-price": float(request.form.get("selling-price", "0")),
                "stock": int(request.form.get("stock", "0")),
                "item-expiration": datetime.strptime(request.form.get("item-expiration", ""), "%Y-%m-%d"),
                "reorder-level": int(request.form.get("reorder-level", "0")),
                "sales-count": int(request.form.get("sales-count", "0")),
                "total-revenue": float(request.form.get("total-revenue", "0")),
            }
            db["products"].update_one({"_id": ObjectId(item_id)}, {"$set": updated_data})

            return redirect('Home.html')

        except Exception as e:
            print("Error in POST /edititem:", str(e))
            return f"Something went wrong: {e}", 500

    product = db["products"].find_one({"_id": ObjectId(item_id)})
    if product:
        if isinstance(product.get("item-expiration"), datetime):
            product["item-expiration"] = product["item-expiration"].strftime("%Y-%m-%d")
    return render_template('edititem.html', page_title="EDIT ITEM", product=product)

   # return "Product not found", 404

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
'''
@app.route('/printreports')
def printreports():
    return render_template('printreports.html', page_title="PRINT REPORTS")
'''

if __name__ == '__main__':
    app.run(debug=False)
