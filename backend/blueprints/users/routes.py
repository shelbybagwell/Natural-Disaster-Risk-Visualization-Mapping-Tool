from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
from bson.objectid import ObjectId
from helpers.user_helper import UserHelper

users_blueprint = Blueprint('users', __name__)

# Create a new user account
@users_blueprint.route('/', methods=['POST'])
def create_user():

    try: 

        data = request.get_json()

        required_fields = ["email", "password", "confirm_password", "full_name"]

        for field in required_fields:
            if field not in data:
                raise Exception(f'Whoops: {field} field is required')

        # Validate/sanitize input
        # if data["username"] == '':
        #     raise Exception('Username is required.')
        # elif not UserHelper.is_valid_username(data["username"]):
        #     raise Exception('Invalid username. Please use 4 to 50 characters: letters, numbers, underscores only...')

        if data['full_name'] == '':
            raise Exception('Name is required.')
        elif not UserHelper.is_valid_name(data['full_name']):
            raise Exception('Invalid name. Use letters, hyphens, or apostrophes only.')

        if data['email'] == '':
            raise Exception('Email is required.')
        elif not UserHelper.is_valid_email(data['email']):
            raise Exception('Invalid email address.')

        if data['password'] == '':
            raise Exception('Password is required.')
        elif not UserHelper.is_strong_password(data['password']):
            raise Exception('Password must be at least 8 characters and include a combination of upper/lowercase letters, numbers and/or special characters.')

        if data['confirm_password'] != data['password']:
            raise Exception('Passwords do not match')

        mongo = current_app.mongo
        users_collection = mongo.db.users

        # Ensure username/email is unique
        # if users_collection.find_one({"username": data["username"]}):
        #     raise Exception(f'Username \'{data["username"]}\' already exists')

        if users_collection.find_one({"email": data["email"]}):
            raise Exception(f'The email address provided has already been used \'{data["email"]}\'')

        hashed_password = UserHelper.hash_password(data['password'])
        
        User = {
            # "username": data['username'],
            "email": data['email'],
            "password": hashed_password,
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


# Fetch a user account by username (email)
@users_blueprint.route('/<username>', methods=['GET'])
def get_user_by_username(username):

    try:

        mongo = current_app.mongo
        users_collection = mongo.db.users

        User = users_collection.find_one({"email": username})

        if not User:
            raise Exception('User not found')

        User["_id"] = str(User["_id"]) # Needed to make Object serializable

        User = UserHelper.sanitize_user_object(User)

        return jsonify(User), 200
    
    except Exception as ex:
        return jsonify({"error": "%s" % ex}), 400


# Fetch a user account by ID
@users_blueprint.route('/id/<id>', methods=['GET'])
def get_user_by_id(id):

    try:

        mongo = current_app.mongo
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
@users_blueprint.route('/id/<id>', methods=['PUT'])
def update_user(id):

    try:

        data = request.get_json()

        mongo = current_app.mongo
        users_collection = mongo.db.users

        User = users_collection.find_one({"_id": ObjectId(id)})

        if not User:
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
        
        User["_id"] = str(User["_id"])

        User = UserHelper.sanitize_user_object(User)

        return jsonify(User), 200

    except Exception as ex:
        return jsonify({"error": "%s" % ex}), 400