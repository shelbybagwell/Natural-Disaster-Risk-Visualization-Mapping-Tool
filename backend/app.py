from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from config import Config
from datetime import datetime
from bson.objectid import ObjectId
from helpers.user_helper import UserHelper

app = Flask(__name__)
app.config.from_object(Config)

mongo = PyMongo(app)  # Initialize MongoDB connection

@app.route('/')
def home():
    return jsonify({"message": ""})

# Create a new user account
@app.route('/user', methods=['POST'])
def create_user():

    try: 

        data = request.get_json()

        required_fields = ["username", "password", "confirm_password", "email", "full_name"]

        for field in required_fields:
            if field not in data:
                return jsonify({"error": f'Whoops: {field} field is required'}), 400

        # Validate/sanitize input
        if data["username"] == '' or not UserHelper.is_valid_username(data["username"]):
            raise Exception('Invalid username. Please use 4 to 50 characters: letters, numbers, underscores only...')

        if data['full_name'] == '' or not UserHelper.is_valid_name(data['full_name']):
            raise Exception('Invalid name. Use letters, hyphens, or apostrophes only.')

        if data['email'] == '' or not UserHelper.is_valid_email(data['email']):
            raise Exception('Invalid email.')

        if not UserHelper.is_strong_password(data['password']):
            raise Exception('Password must be at least 8 characters and include a combination of upper/lowercase letters, numbers and/or special characters.')

        if data['confirm_password'] != data['password']:
            raise Exception('Passwords do not match')

        users_collection = mongo.db.users

        # Ensure username/email is unique
        if users_collection.find_one({"username": data["username"]}):
            raise Exception(f'Username \'{data["username"]}\' already exists')

        if users_collection.find_one({"email": data["email"]}):
            raise Exception(f'The email address provided has already been used \'{data["email"]}\'')

        hashed_password = UserHelper.hash_password(data['password'])
        
        User = {
            "username": data['username'],
            "password": hashed_password,
            "email": data['email'],
            "full_name": data['full_name'],
            "created_at": datetime.now()
        }

        result = users_collection.insert_one(User)
        User["_id"] = str(result.inserted_id)

        User = UserHelper.sanitize_user_object(User)

        return jsonify({
            "message": "Account created successfully", 
            "user": User
            }), 201

    except Exception as ex:
        return jsonify({"error": "%s" % ex}), 400


# Fetch a user account by username
@app.route('/users/<username>', methods=['GET'])
def get_user_by_username(username):

    try:

        users_collection = mongo.db.users

        User = users_collection.find_one({"username": username})

        if not User:
            raise Exception('User not found')

        User["_id"] = str(User["_id"]) # Needed to make Object serializable

        User = UserHelper.sanitize_user_object(User)

        return jsonify(User), 200
    
    except Exception as ex:
        return jsonify({"error": "%s" % ex}), 400


# Fetch a user account by ID
@app.route('/users/id/<id>', methods=['GET'])
def get_user_by_id(id):

    try:

        users_collection = mongo.db.users

        User = users_collection.find_one({"_id": ObjectId(id)})

        if not User:
            raise Exception('User not found')

        User["_id"] = str(User["_id"]) # Needed to make Object serializable

        User = UserHelper.sanitize_user_object(User)

        return jsonify(User), 200

    except Exception as ex:
        return jsonify({"error": "%s" % ex}), 400


# Update a user by ID
@app.route('/users/id/<id>', methods=['PUT'])
def update_user(id):

    try:

        data = request.get_json()

        users_collection = mongo.db.users

        user = users_collection.find_one({"_id": ObjectId(id)})

        if not user:
            raise Exception('User not found')

        updates = {}

        # Validation input
        if "password" in data:

            if not UserHelper.is_strong_password(data["password"]):
                raise Exception('Password must be at least 8 characters and include a combination of upper/lowercase letters, numbers and/or special characters.')

            if data['confirm_password'] != data["password"]:
                raise Exception('Passwords do not match')

            updates["password"] = UserHelper.hash_password(data["password"]) 

        if "full_name" in data:

            if not UserHelper.is_valid_name(data['full_name']):
                raise Exception('Invalid name. Use letters, hyphens, or apostrophes only.')
            
            updates["full_name"] = data["full_name"]

        if "email" in data:

            if not UserHelper.is_valid_email(data['email']):
                raise Exception('Invalid email.')
            
            updates["email"] = data["email"]

        if updates:
            users_collection.update_one(
                {"_id": ObjectId(id)}, 
                {"$set": updates}
            )
        
        User = users_collection.find_one({"_id": ObjectId(id)})

        User["_id"] = str(User["_id"])

        User = UserHelper.sanitize_user_object(User)

        return jsonify(User), 200

    except Exception as ex:
        return jsonify({"error": "%s" % ex}), 400


# Create a new user address
@app.route('/user/address', methods=['POST'])
def create_user_address():

    try:    
        pass
    except Exception as ex:
        return jsonify({"error": "%s" % ex}), 400

# Update a user address by ID
@app.route('/user/address/<id>', methods=['PUT'])
def update_user_address(id):

    try:    
        pass
    except Exception as ex:
        return jsonify({"error": "%s" % ex}), 400

# Fetch a user address by address ID
@app.route('/user/address/<id>', methods=['GET'])
def get_user_address_by_id(id):

    try:
        pass
    except Exception as ex:
        return jsonify({"error": "%s" % ex}), 400

# Fetch a list of user addresses by user ID
@app.route('/user/addresses/<user_id>', methods=['GET'])
def get_addresses_by_user(user_id):

    try:
        pass
    except Exception as ex:
        return jsonify({"error": "%s" % ex}), 400

# Delete a user address by ID
@app.route('/user/address/<id>', methods=['DELETE'])
def delete_user_address():

    try:    
        pass
    except Exception as ex:
        return jsonify({"error": "%s" % ex}), 400

""""
@app.route('/test')
def get_data():
    collection = mongo.db.test_collection
    data = list(collection.find({}, {"_id": 0}))  # Exclude MongoDB ObjectId
    return jsonify(data)
"""

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)