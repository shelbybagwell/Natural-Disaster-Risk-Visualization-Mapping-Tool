from flask import Blueprint, request, jsonify, current_app
from pymongo.errors import DuplicateKeyError, PyMongoError
from datetime import datetime
from bson.objectid import ObjectId
from helpers.address_helper import AddressHelper
from geopy.geocoders import Nominatim

# #configuration for imports
import sys, os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.append(project_root)

from api.FIRMS_API import FIRMS_API_Client
from api.NOAA_API import NOAA_API_Client

packing_blueprint = Blueprint('packing', __name__)

# Fetch a packing list for an address by address ID
@packing_blueprint.route('/<id>', methods=['GET'])
def get_packing_list_by_address_id(id):

    try:
    
        if not id:
            raise Exception('Invalid Address ID')
        
        mongo = current_app.mongo
        packing_collection = mongo.db.packing

        packing_list = packing_collection.find_one({"address_id": id})

        if not packing_list:
            raise Exception('Packing List not found')
        
        return jsonify({"packing list": packing_list}), 200

    except Exception as ex:
        return jsonify({"error": "%s" % ex}), 400

@packing_blueprint.route('/<id>', methods=['PUT'])
def update_packing_list_by_address_id(id):
    try:
    
        data = request.get_json()

        if not id:
            raise Exception('Invalid Address ID')
        
        if 'items' not in data.keys():
            raise Exception('Items is not present in the request!')
        
        if type(data['items']) != list:
            raise Exception('Items is not in list format!')
        
        mongo = current_app.mongo
        packing_collection = mongo.db.packing

        packing_list = packing_collection.find_one({"address_id": id})
        new_items = data['items']
        previous_items = packing_list['items']

        if new_items == previous_items:
            raise Exception('Error! No New Changes Were Made')

        result = packing_collection.update_one({"address_id": id}, {"$set": {"items": new_items}})

        if not packing_list:
            raise Exception('Packing List not found')
        
        return jsonify({
            "packing_list_id": packing_list['_id'],
            "address_id": packing_list['address_id'],
            "previous_items": previous_items,
            "new_items": new_items
        }), 200

    except Exception as ex:
        return jsonify({"error": "%s" % ex}), 400
