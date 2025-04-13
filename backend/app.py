from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from config import Config
from datetime import datetime
# from bson.objectid import ObjectId
# from helpers.user_helper import UserHelper
from helpers.address_helper import AddressHelper
from blueprints.users.routes import users_blueprint
from blueprints.addresses.routes import addresses_blueprint

app = Flask(__name__)
app.config.from_object(Config)

mongo = PyMongo(app)  # Initialize MongoDB connection

# Make Mongo accessible to blueprints
app.mongo = mongo

@app.route('/')
def home():
    return jsonify({"message": ""})


app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(addresses_blueprint, url_prefix="/user/<user_id>/addresses")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)