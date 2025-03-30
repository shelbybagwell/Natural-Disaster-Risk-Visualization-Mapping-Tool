"""
from flask_pymongo import PyMongo

def insert_user(name, age):
    mongo.db.users.insert_one({"name": name, "age": age})

def get_users():
    return list(mongo.db.users.find({}, {"_id": 0}))  # Exclude ObjectId

"""