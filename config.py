from http import client
import pymongo
import certifi


con_str = 'mongodb+srv://Naqui17:Mackman17!!@cluster0.nakll.mongodb.net/?retryWrites=true&w=majority'

client = pymongo.MongoClient(con_str, tlsCAFile=certifi.where())

db = client.get_database("ClothingStore")


