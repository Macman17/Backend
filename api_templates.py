from pydantic import Optional, Field
from bson import ObjectId
from config import db

class User(db.users):
    
    firstName: str
    lastName: str
    userName = db.StringField()
    streetAddress = db.StringField()
    city = db.StringField()
    state = db.StringField()
    country = db.StringField()
    zipCode = db.IntField()
    emailAdress = db.StringField()
    password = db.StringField()

    
    def to_json(self):

        return{
            
            "firstName": self.firstName,
            "lastName": self.lastName,
            "userName": self.userName,
            "streetAddress": self.streetAddress,
            "city": self.city,
            "state": self.state,
            "country": self.country,
            "zipCode": self.zipCode,
            "emailAddress": self.emailAdress,
            "password": self.password
        }

    def to_bson(self):
        data = self.dict(by_alias=True, exclude_none=True)
        if data["_id"] is None:
            data.pop("_id")
        return data
class Product(db.product):
    product_id = db.IntField()
    title = db.StringField()
    styleType = db.StringField()
    image = db.StringField()
    price = db.IntField()
    discount = db.IntField()
    gender = db.StringField()

    def to_json(self):
        return{
            "product_id": self.product_id,
            "title": self.title,
            "styleType": self.styleType,
            "image": self.image,
            "price": self.price,
            "discount": self.discount,
            "gender": self.gender

        } 
    def to_bson(self):
        data = self.dict(by_alias=True, exclude_none=True)
        if data["_id"] is None:
            data.pop("_id")
        return data    

class CouponCode(db.couponCode):
    coupon_id = db.IntField()
    code = db.StringField()
    discount = db.IntField()

    def to_json(self):
        return{
            "coupon_id": self.coupon_id,
            "code": self.code,
            "discount": self.discount
        }
    def to_bson(self):
        data = self.dict(by_alias=True, exclude_none=True)
        if data["_id"] is None:
            data.pop("_id")
        return data


