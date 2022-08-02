
from re import L
from unittest import result
from bson import ObjectId
from itertools import product
from flask import Flask, render_template, request, abort, session
import json

from config import db
from flask_cors import CORS



app = Flask('server')
CORS(app) #disable CORS

@app.get('/')
def index():
    if 'username' in session:
        return 'You are logged in as' + session['username']
    return render_template('ClothingRoutes.jsx')    

@app.get('/login')
def login():
    return ''

    
#USER INFO CRUD
# USER Create
@app.post("/api/user")
def create_user():
    cursor = db.user
    id = cursor.insert_one({
        'name': request.json['name'],
        'email': request.json['email'],
        'password': request.json['password'],
        'country': request.json['country'],
        'city': request.json['city'],
        'zip': request.json['zip']
    })
    return 'User created'

#USER READ
@app.get("/api/users")
def get_users():
    users = []

    cursor = db.user.find({})
    
    for user in cursor:
        users.append({
            '_id': str(ObjectId(user['_id'])),
            'name': user['name'],
            'email': user['email'],
            'password': user['password'],
            'country': user['country'],
            'city': user['city'],
            'zip': user['zip']
        })

    return json.dumps(users)

@app.get('/api/user/<id>')
def get_user(id):
    user = []

    user = db.user.find_one({'_id': ObjectId(id)})

    return json.dumps({
        'name': user['name'],
        'email': user['email'],
        'password': user['password'],
        'country': user['country'],
        'city': user['city'],
        'zip': user['zip']
    })

#USER DELETE
@app.route('/api/user/<id>', methods=['DELETE'])
def delete_User(id):
    db.user.delete_one({'_id': ObjectId(id)})
    print(id)
    return json.dumps({'msg': 'User deleted'})

#USER UPDATE
@app.route('/api/users/<id>', methods=['PUT'])
def update_User(id):
    print(id)
    print(request.json)

    cursor = db.user

    cursor.update_one({'_id': ObjectId(id)}, {'$set': {
    'name': cursor['name'],
    'email': cursor['email'],
    'password': cursor['password'],
    'country': cursor['country'],
    'city': cursor['city'],
    'zip': cursor['zip']
    }})

    return json.dumps({'msg': 'UserUpdated'})




#admin page
@app.get("/api/admin")
def  get_add():

    return

@app.get("/api/catalog")
def get_catalog():
    cursor = db.product.find({}) #get all
    all_products = []

    for prod in cursor:
        prod["_id"] = str(prod["_id"])
        all_products.append(prod)

    return json.dumps(all_products)  
    

@app.route("/api/catalog/cheapest")
def get_cheapest():    
    print("cheapest product")

    db_prod= db.product.find({})
    solution= db_prod[0]
    for prod in db_prod:
        if prod["price"] < solution["price"]:
            solution = prod


    solution["_id"] = str(solution["_id"])       
    return json.dumps(solution)

@app.route("/api/catalog/total")
def get_total(): 
    print("total")

    db_prod= db.product.find({})
    total = 0
    for prod in db_prod:
        total += prod["price"]

    return json.dumps(total) 

#Product Section
#Product Create
@app.post("/api/catalog")
def save_product():
    product = request.get_json()
    db.product.insert_one(product)

    if not "title" in product or len(product["title"]) < 5:
        return abort(400, "Title should contains at least 5 chars.")


    if not "image" in product or len(product["image"]) < 1:
        return abort(400, "Image is required.")

    if not "styleType" in product or len(product["styleType"]) < 1:
        return abort(400, "Style type is required.")   


    print("Product saved!")
    print(product)

    #fix the id issue
    product["_id"] = str(product["_id"])

    return json.dumps(product) # crash

#Product Read
@app.route("/api/products/<id>")
def find_product(id):
    prod = db.product.find_one({"_id": ObjectId(id)})


    
    if not ObjectId.is_valid(id):
        return abort(400, "ObjectId is not an ID.") 

    prod["_id"] = str(prod["_id"]) 

    return json.dumps(prod)


@app.route("/api/product/styletype")
def get_catagories():
    cursor= db.product.find({})
    catagories = []  
    

    for prod in cursor:
        cat = prod["styleType"]
        if not cat in catagories:
            catagories.append(cat)

    catagories["_id"] = str(catagories["_id"]) 
    return json.dumps(catagories)

@app.route("/api/product/styletype/<cat_name>")

def get_title(cat_name):
    cursor= db.product.find({"styleType": cat_name})
    results = []

    for prod in cursor:
        if prod["styleType"].lower() == cat_name.lower() :
            results.append(prod)
    prod["_id"] = str(prod["_id"]) 
    return json.dumps(results)    

#update product
@app.put("/api/product/<id>")
def update_product(id):
    print(id)
    print(request.json)
    cursor = db.product
    
    cursor.update_one({'_id': ObjectId(id)}, {'$set': {
    'title': cursor['title'],
    'stock': cursor['stock'],
    'price': cursor['price'],
    'image': cursor['image'],
    'styleType': cursor['styleType'],
    'gender': cursor['gender']
    }})

    cursor["_id"] = str(cursor["_id"])

    return json.dumps({'msg': 'UserUpdated'})

#Delete Product
@app.route('/api/product/<id>', methods=['DELETE'])
def delete_product(id):
    db.product.delete_one({'_id': ObjectId(id)})
    print(id)
    
    return json.dumps({'msg': 'User deleted'})


#Coupon Code Section

#Get Coupon Codes
@app.get("/api/couponCode")
def get_coupon():

    cursor= db.couponCode.find({})
    results= []

    for coupon in cursor:
        coupon["_id"] = str(coupon["_id"]) 
        results.append(coupon)
        
    return json.dumps(results)

#Valid Coupon codes
@app.get("/api/couponCode/<code>")
def get_by_code_coupon(code):

    coupon = db.couponCode.find_one({"code": code})
    if not coupon:
        return abort(400, "Invalid coupon code")

    
    code["_id"] = str(code["_id"]) 
    return json.dumps(coupon)

#Post Coupon Code
@app.post("/api/couponCode")
def save_coupon():
    coupon = request.get_json()

    if not "code" in coupon or len(coupon["code"]) < 5:
        return abort(400, "Code is required and should contains at least 5 chars.")
    
    if not "discount" in coupon:
        return abort(400, "Discount is required.")

    if type(coupon["discount"]) != int and type(coupon["discount"]) != float:
        return abort(400, "Discount is required and should a valid number.")
        
    if coupon["discount"] < 0 or coupon["discount"] > 31:
        return abort(400, "Discount should be lower than 31.")

    db.couponCode.insert_one(coupon)
    coupon["_id"] = str(coupon["_id"])
    return json.dumps(coupon)

   
if __name__ == '__main__':  
    app.run(debug=True)