from flask import Flask, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from datetime import datetime, timedelta
from blueprints.auth.routes import auth_blueprint
from blueprints.users.routes import users_blueprint
from blueprints.addresses.routes import addresses_blueprint
from blueprints.packing.routes import packing_blueprint
import os

app = Flask(__name__)
app.config.from_object(Config)

mongo = PyMongo(app)  # Initialize MongoDB connection

# Make Mongo accessible to blueprints
app.mongo = mongo

# Setup CORS to allow credentials (cookies)
CORS(app, supports_credentials=True) #  origins=["http://localhost:4200"], 

# Setup JWT
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False  # (Can enable later for CSRF protection)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

jwt = JWTManager(app)

app.register_blueprint(auth_blueprint, url_prefix="/auth")
app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(addresses_blueprint, url_prefix="/addresses")
app.register_blueprint(packing_blueprint, url_prefix="/packing")

@app.route('/')
def home():
    return jsonify({"message": ""})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)