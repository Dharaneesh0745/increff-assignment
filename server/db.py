from pymongo import MongoClient
from bson.objectid import ObjectId

MONGO_URI = "mongodb+srv://dharaneesh5577:Dhoni_007@cluster0.rgafzk3.mongodb.net/products"

client = MongoClient(MONGO_URI)

db = client["products"]

def get_collection(collection_name: str):
    return db[collection_name]

def serialize_objectid(item):
    if isinstance(item, dict):
        for key, value in item.items():
            if isinstance(value, ObjectId):
                item[key] = str(value)
            elif isinstance(value, dict):
                item[key] = serialize_objectid(value)
    return item