from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
from bson.objectid import ObjectId
from helpers.address_helper import AddressHelper

addresses_blueprint = Blueprint('addresses', __name__)

# Create a new user address
@addresses_blueprint.route('/', methods=['POST'])
def create_user_address(user_id):

    try:    

        data = request.get_json()

        # Required fields: street_1, city, state, zip, country, latitude, longitude, address_name, is_primary
        # Optional fields: street_2

        if not user_id:
            raise Exception('Invalid user ID')

        required_fields = ["street_1", "city", "state", "zip", "country", "address_name", "is_primary"]

        for field in required_fields:
            if field not in data:
                raise Exception(f'Whoops: {field} field is required')

        # Validate address
        if data["street_1"] == '' :
            raise Exception('Street address is required.')
        elif not AddressHelper.is_valid_street(data["street_1"]):
            raise Exception('Please limit each street address to 100 characters')

        if data["street_2"]:
            if not AddressHelper.is_valid_street(data["street_2"]):
                raise Exception('Please limit each street address to 100 characters')

        # TO DO: complete validation and save address to DB
        mongo = current_app.mongo
        address_collection = mongo.db.users


    except Exception as ex:
        return jsonify({"error": "%s" % ex}), 400

# Update a user address by ID
@addresses_blueprint.route('/<id>', methods=['PUT'])
def update_user_address(id):

    try:    
        pass
    except Exception as ex:
        return jsonify({"error": "%s" % ex}), 400

# Fetch a user address by address ID
@addresses_blueprint.route('/<id>', methods=['GET'])
def get_user_address_by_id(id):

    try:
        pass
    except Exception as ex:
        return jsonify({"error": "%s" % ex}), 400

# Fetch a list of user addresses by user ID
@addresses_blueprint.route('/list', methods=['GET'])
def get_addresses_by_user(user_id):

    try:
        pass
    except Exception as ex:
        return jsonify({"error": "%s" % ex}), 400

# Delete a user address by ID
@addresses_blueprint.route('/<id>', methods=['DELETE'])
def delete_user_address():

    try:    
        pass
    except Exception as ex:
        return jsonify({"error": "%s" % ex}), 400