from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from config import Config
from datetime import datetime
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object(Config)

mongo = PyMongo(app)  # Initialize MongoDB connection

@app.route('/')
def home():
    return jsonify({"message": "Flask connected to MongoDB!"})

# Create a new user account
@app.route('/user', methods=['POST'])
def create_user():

    data = request.get_json()

    required_fields = ["username", "password", "email", "full_name"]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f'Whoops: {field} field is required'}), 400

    # TO DO: Validate/sanitize input

    users_collection = mongo.db.users

    # Ensure username 
    if users_collection.find_one({"username": data["username"]}):
        return jsonify({"error": f'Username \'{data["username"]}\' already exists'}), 409


    hashed_password = generate_password_hash(data["password"])
    
    User = {
        "username": data["username"],
        "password": hashed_password,
        "email": data["email"],
        "full_name": data["full_name"],
        "created_at": datetime.now()
    }

    result = users_collection.insert_one(User)
    User["_id"] = str(result.inserted_id)

    if "password" in User:
        del User["password"]  # remove password

    return jsonify({
        "message": "Account created successfully", 
        "user": User
        }), 201

# Fetch a user account by username
@app.route('/users/<username>', methods=['GET'])
def get_user_by_username(username):

    users_collection = mongo.db.users

    User = users_collection.find_one({"username": username})

    if not User:
        return jsonify({"error": "User not found"}), 404

    User["_id"] = str(User["_id"]) # Needed to make Object serializable

    if "password" in User:
        del User["password"]  # remove password

    return jsonify(User), 200

# Fetch a user account by ID
@app.route('/users/id/<id>', methods=['GET'])
def get_user_by_id(id):

    users_collection = mongo.db.users

    User = users_collection.find_one({"_id": ObjectId(id)})

    if not User:
        return jsonify({"error": "User not found"}), 404

    User["_id"] = str(User["_id"]) # Needed to make Object serializable

    if "password" in User:
        del User["password"]  # remove password

    return jsonify(User), 200


# Update a user by ID
@app.route('/users/id/<id>', methods=['PUT'])
def update_user(id):

    data = request.get_json()

    users_collection = mongo.db.users

    user = users_collection.find_one({"_id": ObjectId(id)})

    if not user:
        return jsonify({"error": "User not found"}), 404

    updates = {}

    # TO DO: add validation here

    for field in ["email", "full_name", "password"]:
        if field in data:
            if field == "password":
                updates[field] = generate_password_hash(data[field]) 
            else: 
                updates[field] = data[field]

    if updates:
        users_collection.update_one(
            {"_id": ObjectId(id)}, 
            {"$set": updates}
        )
    
    User = users_collection.find_one({"_id": ObjectId(id)})

    User["_id"] = str(User["_id"])

    if "password" in User:
        del User["password"]  # remove password

    return jsonify(User), 200

""""
@app.route('/test')
def get_data():
    collection = mongo.db.test_collection
    data = list(collection.find({}, {"_id": 0}))  # Exclude MongoDB ObjectId
    return jsonify(data)
"""

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)