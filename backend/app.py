from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from config import Config
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object(Config)

mongo = PyMongo(app)  # Initialize MongoDB connection

@app.route('/')
def home():
    return jsonify({"message": "Flask connected to MongoDB!"})

@app.route('/user', methods=['POST'])
def create_user():

    data = request.get_json()

    # ["username", "password", "email", "full_name"]

    required_fields = ["username", "password", "email", "full_name"]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f'Whoops: {field} field is required'}), 400

    # TO DO: Validate/sanitize input

    users_collection = mongo.db.users

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


""""
@app.route('/test')
def get_data():
    collection = mongo.db.test_collection
    data = list(collection.find({}, {"_id": 0}))  # Exclude MongoDB ObjectId
    return jsonify(data)
"""

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)