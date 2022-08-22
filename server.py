import os
from unittest import result
from bson import ObjectId
from itertools import product
from flask import Flask, render_template, request, abort, session, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import json

from config import db
from flask_cors import CORS

UPLOAD_FOLDER = 'public/img'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask('server')
CORS(app) #disable CORS
app.config['SECRET_KEY'] = 'clothingstore' 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' in session:
        return 'You are logged in as' + session['username']
    return render_template('ClothingRoutes.jsx')    
 #photo handling
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return json.dumps({"msg":"Photo uploaded!!"})
    
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
        
@app.post('/api/login')
def login():
    credentials = request.get_json()

    name = credentials['name']
    password = credentials['password']

    users = []
    user_founded = ''
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

    response = False
    for user in users:
        if name in user['name']:

            if password == user["password"]:
                print('** SAME PASSWORD*')
                user_founded = user
                response = True
                break
            else:
                print('** PASSWORD WRONG')
            break

    if response is not False:
        return json.dumps(user_founded), 200
    else:
        return "User not found"


#USER INFO CRUD
# USER Create
@app.post("/api/user")
def create_user():
    product = request.get_json()

    db.user.insert_one(product)

    if not "name" in product or len(product["name"]) < 2:
        return abort(400, "You must enter your name!")

    if not "email" in product:
         return abort(400, "Email address is required.")

    if not "zip" in product or len(product["zip"]) < 5:
         return abort(400, "Zip code requires at least 5 chars.")

    if not type(product["zip"]) != float and type(product["zip"]) != int:
        return abort(400, "Must be a valid number.")

    if product["zip"] == 0:
        return abort(400, "Must be higher than 0.")

    if not "country" in product or len(product["country"]) < 2:
        return abort(400, "Country is required.")

#     if not "city" in product or len(product["city"]) < 2:
#         return abort(400, "City is required.")

#     if not "password" in product or len(product["password"]) < 4:
#         return abort(400, "Password is required.")

#     if not type(product["password"]) not in [type(float),type(int)]:
#         return abort(400, "You must have at least 1 number in password.")

#     return json.dumps(id)



#USER READ
# @app.get("/api/users")
# def get_users():
#     users = []

#     cursor = db.user.find({})

#     for user in cursor:
#         users.append({
#             '_id': str(ObjectId(user['_id'])),
#             'name': user['name'],
#             'email': user['email'],
#             'password': user['password'],
#             'country': user['country'],
#             'city': user['city'],
#             'zip': user['zip']
#         })

#     return json.dumps(users)



#USER DELETE
@app.route('/api/user/<id>', methods=['DELETE'])
def delete_User(id):
    db.user.delete_one({'_id': ObjectId(id)})
    print(id)
    return json.dumps({'msg': 'User deleted'})

#admin page
# @app.get("/api/admin")
# def  get_add():

#     return



#USER DELETE
@app.route('/api/user/<id>', methods=['DELETE'])
def deleteUser(id):
    db.user.delete_one({'_id': ObjectId(id)})
    print(id)
    return json.dumps({'msg': 'User deleted'})

@app.route('/api/user/<id>', methods=['PUT'])
#USER UPDATE
def updateUser(id):
    print(id)
    print(request.json)

    cursor = db.user

    cursor.update_one({'_id': ObjectId(id)}, {'$set': {
    'name': request.json['name'],
    'email': request.json['email'],
    'password': request.json['password'],
    'country': request.json['country'],
    'city': request.json['city'],
    'zip': request.json['zip']
    }})

    return json.dumps({'msg': 'UserUpdated'})




    return jsonify(all_products)


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
    cursor = db.product

    id = cursor.insert_one({
        'title': request.json['title'],
        'price': request.json['price'],
        'image': request.json['image'],
        'styleType': request.json['styleType'],
        'gender': request.json['gender'],
        'stock': request.json['stock'],
        'discount': request.json['discount'],
        'category': request.json['category'],

    })
    return jsonify(str(id.inserted_id))

    # id = cursor.insert_one({'_id': ObjectId(id)}, {'$set': {
    # 'title': cursor['title'],
    # 'price': cursor['price'],
    # 'image': cursor['image'],
    # 'styleType': cursor['styleType'],
    # 'gender': cursor['gender']
    # }})

    # if not "title" in cursor or len(cursor["title"]) < 5:
    #     return abort(400, "Title should contains at least 5 chars.")

    # if not "price" in cursor:
    #     return abort(400, "Price is required.")

    # if not type(cursor["price"]) != float and type(cursor["price"]) != int:
    #     return abort(400, "Must be a valid number.")

    # if cursor["price"] <= 0:
    #     return abort(400, "Must be higher than 0.")

    # if not "image" in cursor or len(cursor["image"]) < 1:
    #     return abort(400, "Image is required.")

    # if not "styleType" in cursor or len(cursor["styleType"]) < 1:
    #     return abort(400, "Style Type is required.")

    # if not "gender" in cursor or len(cursor["gender"]) < 1:
    #     return abort(400, "Gender is required.")


    # return json.dumps(id)

#Product Read
@app.get("/api/catalog")
def get_catalog():
    cursor = db.product.find({}) #get all
    all_products = []

    for prod in cursor:
        prod["_id"] = str(prod["_id"])
        all_products.append(prod)

    return json.dumps(all_products)  
@app.route("/api/catalog/<id>")

def find_product(id):
    prod = db.product.find_one({"_id": ObjectId(id)})

    if not ObjectId.is_valid(id):
        return abort(400, "ObjectId is not an ID.")

    # prod["_id"] = str(prod["_id"])

    return jsonify({
        'title': prod['title'],
        'price': prod['price'],
        'image': prod['image'],
        'styleType': prod['styleType'],
        'gender': prod['gender'],
        'stock': prod['stock'],
        'discount': prod['discount'],
        'category': prod['category'],
    })


@app.route("/api/catalog/styletype")
def get_catagories():
    cursor= db.product.find({})
    catagories = []


    for prod in cursor:
        cat = prod["styleType"]
        if not cat in catagories:
            catagories.append(cat)

    catagories["_id"] = str(catagories["_id"])
    return json.dumps(catagories)

@app.route("/api/catalog/styletype/<cat_name>")

def get_title(cat_name):
    cursor= db.product.find({"styleType": cat_name})
    results = []

    for prod in cursor:
        if prod["styleType"].lower() == cat_name.lower() :
            results.append(prod)
    prod["_id"] = str(prod["_id"])
    return json.dumps(results)

#update product
@app.route("/api/product/<id>",  methods=['PUT'])
def update_product(id):
    print(id)
    print(request.json)
    cursor = db.product

    cursor.update_one({'_id': ObjectId(id)}, {'$set': {
    'title': request.json['title'],
    'price': request.json['price'],
    'image': request.json['image'],
    'styleType': request.json['styleType'],
    'gender': request.json['gender'],
    'stock': request.json['stock'],
    'discount': request.json['discount'],
    'category': request.json['category']
    }})

    return json.dumps({'msg': 'ProductUpdated'})


    # if not "title" in cursor or len(cursor["title"]) < 5:
    #     return abort(400, "Title should contains at least 5 chars.")

    # if not "price" in cursor:
    #     return abort(400, "Price is required.")

    # if not type(cursor["price"]) != float and type(cursor["price"]) != int:
    #     return abort(400, "Must be a valid number.")

    # if cursor["price"] <= 0:
    #     return abort(400, "Must be higher than 0.")

    # if not "image" in cursor or len(cursor["image"]) < 1:
    #     return abort(400, "Image is required.")

    # if not "styleType" in cursor or len(cursor["styleType"]) < 1:
    #     return abort(400, "Style Type is required.")

    # if not "gender" in cursor or len(cursor["gender"]) < 1:
    #     return abort(400, "Gender is required.")



    return json.dumps({'msg': 'UserUpdated'})

#Delete Product
@app.route('/api/catalog/<id>', methods=['DELETE'])
def delete_product(id):
    db.product.delete_one({'_id': ObjectId(id)})
    print(id)

    return json.dumps({'msg': 'User deleted'})


    

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
@app.get("/api/couponCode/<id>")
def get_coupon_by_id(id):
    print(F'id code is {id}')

    coupon = db.couponCode.find_one({"_id": ObjectId(id)})
    print(f'coupon: {coupon}')

    if not coupon:
         return abort(400, "Invalid coupon code")

    return json.dumps({
        'code': coupon['code'],
        'discount': coupon['discount']
    })
 
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

#Update Coupon

@app.put("/api/couponCode/<id>")
def update_coupon(id):
    print(id)
    print(request.json)
    cursor = db.couponCode

    cursor.update_one({'_id': ObjectId(id)}, {'$set': {
    'code': cursor['code'],
    'discount': cursor['discount']
    }})

#Delete Coupon
@app.route('/api/couponCode/<id>', methods=['DELETE'])
def delete_coupon(id):
    db.couponCode.delete_one({'_id': ObjectId(id)})
    print(id)
    return json.dumps({'msg': 'Coupon deleted'})

if __name__ == '__main__':
    app.run(debug=True)