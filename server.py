from bson import ObjectId
from itertools import product
from flask import Flask, jsonify, request, abort
import json
from config import db
from flask_cors import CORS



app = Flask('server')
CORS(app) #disable CORS

#admin page
@app.get("/api/admin")
def  get_add():

    return
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
    return jsonify(str(id.inserted_id))

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

    # return users
    # return json.dumps(users)
    return jsonify(users)


@app.get('/api/user/<id>')
def get_user(id):
    user = []

    user = db.user.find_one({'_id': ObjectId(id)})

    # for user in cursor:
    #     users.append({
    #         '_id': str(ObjectId(user['_id'])),
    #         'name': user['name'],
    #         'email': user['email'],
    #         'password': user['password'],
    #         'country': user['country'],
    #         'city': user['city'],
    #         'zip': user['zip']
    #     })
    # print(".... ",users)

    return json.dumps({
        'name': user['name'],
        'email': user['email'],
        'password': user['password'],
        'country': user['country'],
        'city': user['city'],
        'zip': user['zip']
    })

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
        return jsonify(user_founded), 200
    else:
        return "User not found"


#USER DELETE
@app.route('/api/user/<id>', methods=['DELETE'])
def deleteUser(id):
    db.user.delete_one({'_id': ObjectId(id)})
    print(id)
    return jsonify({'msg': 'User deleted'})

@app.route('/api/user/<id>', methods=['PUT'])
#USER UPDATE

def updateUser(id):
    print(f'id: {id}')
    print(f'request.json {request.json}')

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


@app.get("/api/catalog")
def get_catalog():
    cursor = db.product.find({}) #get all
    all_products = []

    for prod in cursor:
        prod["_id"] = str(prod["_id"])
        all_products.append(prod)

    return json.dumps(all_products)

@app.post("/api/catalog")
def save_product():
    product = request.get_json()
    db.product.insert_one(product)

    if not "title" in product or len(product["title"]) < 5:
        return abort(400, "Title should contains at least 5 chars.")


    if not "image" in product or len(product["image"]) < 1:
        return abort(400, "Image is required.")

    if not "styleType" in product or len(product["category"]) < 1:
        return abort(400, "Style type is required.")


    print("Product saved!")
    print(product)

    #fix the id issue
    product["_id"] = str(product["_id"])

    return json.dumps(product) # crash


@app.route("/api/catalog/cheapest")
def get_cheapest():
    print("cheapest product")

    db_prod= db.products.find({})
    solution= db_prod[0]
    for prod in db_prod:
        if prod["unitPrice"] < solution["unitPrice"]:
            solution = prod


    solution["_id"] = str(solution["_id"])
    return json.dumps(solution)

@app.route("/api/catalog/total")
def get_total():
    print("total")

    db_prod= db.product.find({})
    total = 0
    for prod in db_prod:
        total += prod["unitPrice"]

    return json.dumps(total)

#Product Section
@app.route("/api/products/<id>")
def find_product(id):
    prod = db.product.find_one({"_id": ObjectId(id)})



    if not ObjectId.is_valid(id):
        return abort(400, "ObjectId is not an ID.")

    prod["_id"] = str(prod["_id"])

    return json.dumps(prod)


@app.route("/api/products/category")
def get_catagories():
    cursor= db.product.find({})
    catagories = []


    for prod in cursor:
        cat = prod["category"]
        if not cat in catagories:
            catagories.append(cat)

    catagories["_id"] = str(catagories["_id"])
    return json.dumps(catagories)

@app.route("/api/products/category/<cat_name>")

def get_title(cat_name):
    cursor= db.product.find({"category": cat_name})
    results = []

    for prod in cursor:
        if prod["category"].lower() == cat_name.lower() :
            results.append(prod)
    prod["_id"] = str(prod["_id"])
    return json.dumps(results)


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
def get_user_by_id(id):
    print(f'id code is {id}')

    coupon = db.couponCode.find_one({"_id": ObjectId(id)})
    print(f'coupon: {coupon}')

    # if not coupon:
    #     return abort(400, "Invalid coupon code")

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


if __name__ == '__main__':
    app.run(debug=True)