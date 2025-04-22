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

addresses_blueprint = Blueprint('addresses', __name__)

# Create a new user address
@addresses_blueprint.route('/user/<user_id>', methods=['POST'])
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
            raise Exception('Street address is required')
        elif not AddressHelper.is_valid_street(data["street_1"]):
            raise Exception('Please limit each street address to 100 characters')

        if data["street_2"]:
            if not AddressHelper.is_valid_street(data["street_2"]):
                raise Exception('Please limit each street address to 100 characters')
        else:
            data["street_2"] = ""

        if data["city"] == '' :
            raise Exception('City is required')
        elif not AddressHelper.is_valid_city(data["city"]):
            raise Exception('Please provide a valid city')

        if data["state"] == '' :
            raise Exception('State is required')
        elif not AddressHelper.is_valid_state(data["state"]):
            raise Exception('Please provide a valid state')

        if data["zip"] == '' :
            raise Exception('Zip Code is required')
        elif not AddressHelper.is_valid_zip_code(data["zip"]):
            raise Exception('Please provide a valid zip code')
        
        if data["address_name"] == '' :
            raise Exception('Address Name is required')
        elif not AddressHelper.is_valid_address_name(data["address_name"]):
            raise Exception('Please provide a valid name for this address')

        # Cast primary to boolean value
        data["is_primary"] = bool(data["is_primary"])

        # Addresses will be limited to US for now 
        data["country"] = 'USA'

        # Validate address by converting to lat/long coordinates
        strAddress = data['street_1'] + ', ' + data['city'] + ', ' + data['state'] + ' ' + data['zip']
        geolocator = Nominatim(user_agent='user_address', timeout=5)
        location = geolocator.geocode(strAddress)

        if (location is None):
            raise Exception('Unable to verify this address')

        longitude = location.longitude
        latitude = location.latitude

        if not AddressHelper.is_valid_lat_long(latitude, longitude):
            raise Exception('Unable to validate this address')

        mongo = current_app.mongo
        address_collection = mongo.db.addresses
        packing_collection = mongo.db.packing

        Address = {
            "user_id": user_id,
            "street_1": data["street_1"],
            "street_2": data["street_2"],
            "city": data["city"],
            "state": data["state"],
            "zip": data["zip"],
            "latitude" : latitude, 
            "longitude" : longitude, 
            "address_name": data["address_name"],
            "is_primary": data["is_primary"], # Enforce one address as primary?
            "created_at": datetime.now()
        }

        result = address_collection.insert_one(Address)
        Address["_id"] = str(result.inserted_id)

        default_packing_list = {
            "address_id": str(result.inserted_id),
            "items": [
                "Important Documents (IDs, passports, insurance, medical records)",
                "Medications & Prescriptions",
                "First Aid Kit",
                "Multipurpose Tool",
                "Water",
                "Non-perishable food",
                "Phone",
                "Charger",
                "Power Bank",
                "Cash",
                "Maps"
            ]
        }
        packing = packing_collection.insert_one(default_packing_list)

        return jsonify({
            "message": "Address created successfully", 
            "address": Address,
            "packing": str(packing.inserted_id)
            }), 201

    except PyMongoError as ex:
        return jsonify({"error": "%s" % ex}), 400
    except Exception as ex:
        return jsonify({"error": "%s" % ex}), 400
    

# Update a user address by ID
@addresses_blueprint.route('/<id>', methods=['PUT'])
def update_user_address(id):

    try:    

        data = request.get_json()

        if not id:
            raise Exception('Invalid Address ID')
        
        mongo = current_app.mongo
        address_collection = mongo.db.addresses

        Address = address_collection.find_one({"_id": ObjectId(id)})

        if not Address:
            raise Exception('Address not found')

        if "street_1" in data:

            if not AddressHelper.is_valid_street(data['street_1']):
                raise Exception('Please limit each street address to 100 characters')
            
            Address["street_1"] = data["street_1"]

        if "street_2" in data:

            if not AddressHelper.is_valid_street(data['street_2']):
                raise Exception('Please limit each street address to 100 characters')
            
            Address["street_2"] = data["street_2"]

        if "city" in data:

            if not AddressHelper.is_valid_city(data['city']):
                raise Exception('Please provide a valid city')
            
            Address["city"] = data["city"]

        if "zip" in data:

            if not AddressHelper.is_valid_zip_code(data['zip']):
                raise Exception('Please provide a valid zip code')
            
            Address["zip"] = data["zip"]

        if "address_name" in data:

            if not AddressHelper.is_valid_address_name(data['address_name']):
                raise Exception('Please provide a valid zip code')
            
            Address["address_name"] = data["address_name"]

        if "is_primary" in data:            
            Address["is_primary"] = bool(data["is_primary"])

        # Validate address by converting to lat/long coordinates
        strAddress = AddressHelper.toString(Address)
        geolocator = Nominatim(user_agent='user_address', timeout=5)
        location = geolocator.geocode(strAddress)

        if (location is None):
            raise Exception('Unable to verify this address')

        Address["longitude"] = location.longitude
        Address["latitude"] = location.latitude

        if not AddressHelper.is_valid_lat_long(Address["latitude"], Address["longitude"]):
            raise Exception('Unable to validate this address')

        address_collection.update_one(
            {"_id": ObjectId(id)}, 
            {"$set": Address}
        )

        Address["_id"] = str(Address["_id"])

        return jsonify({
            "message": "Address updated successfully", 
            "address": Address
            }), 200

    except Exception as ex:
        return jsonify({"error": "%s" % ex}), 400

# Fetch a user address by address ID
@addresses_blueprint.route('/<id>', methods=['GET'])
def get_user_address_by_id(id):

    try:
        
        data = request.get_json()

        if not id:
            raise Exception('Invalid Address ID')
        
        mongo = current_app.mongo
        address_collection = mongo.db.addresses

        Address = address_collection.find_one({"_id": ObjectId(id)})

        if not Address:
            raise Exception('Address not found')
        
        return jsonify({"address": Address}), 200

    except Exception as ex:
        return jsonify({"error": "%s" % ex}), 400

# Fetch a list of user addresses by user ID
@addresses_blueprint.route('/list/user/<user_id>', methods=['GET'])
def get_addresses_by_user(user_id):

    try:

        if not user_id:
            raise Exception('Invalid User ID')

        mongo = current_app.mongo
        address_collection = mongo.db.addresses

        addresses = list(address_collection.find({"user_id": ObjectId(user_id)}))

        # Convert ObjectId fields to strings for JSON serialization
        if addresses:
            for addr in addresses:
                addr["_id"] = str(addr["_id"])
                addr["user_id"] = str(addr["user_id"])

        return jsonify({"data": addresses}), 200

    except Exception as ex:
        return jsonify({"error": "%s" % ex}), 400

# Delete a user address by ID
@addresses_blueprint.route('/<id>', methods=['DELETE'])
def delete_user_address(id):

    try:    

        data = request.get_json()

        if not id:
            raise Exception('Invalid Address ID')

        mongo = current_app.mongo
        address_collection = mongo.db.addresses
        
        result = address_collection.delete_one({"_id": ObjectId(id)})

        if result.deleted_count == 0:
            raise Exception('Address not found for deletion')

        return jsonify({"message": "Address deleted successfully"}), 200
        
    except Exception as ex:
        return jsonify({"error": "%s" % ex}), 400
    

@addresses_blueprint.route('/search', methods=['POST'])
def search():

        data = request.get_json()
        street_address = data['street_address']
        address_line2 = data['address_line2']
        city = data['city']
        state = data['state']
        zip_code = data['zip']

        #geopy the address to get lon/lat
        strAddress = street_address + ', ' + city + ', ' + state + ' ' + zip_code
        geolocator = Nominatim(user_agent='user_address', timeout=5)
        location = geolocator.geocode(strAddress)
        lon = location.longitude
        lat = location.latitude
    
        #fire features nearby from FIRMS Api
        f = FIRMS_API_Client()
        area_bound = 5
        address_data = f.get_data(bound=[lat + area_bound, lon - area_bound, lat - area_bound, lon + area_bound])

        #general alerts from NOAA_API
        n = NOAA_API_Client()
        zones = n.get_state_zone_ids(state=state)
        county = location.raw['display_name'].split(',')
        for c in county:
            if 'county' in c.lower():
                county = c.lower().replace('county', '').replace(' ', '')
        
        county_codes = []
        for z in zones:
            if county in z['name'].lower():
                county_codes.append(z)

        alerts = []
        for c in county_codes:
            data = n.get_alerts_for_zone(c['zone_id'])
            data['name'] = c['name']
            alerts.append(data)

        return jsonify({
            'full_address': strAddress,
            'street_address': street_address,
            'address_line2': address_line2,
            'city': city,
            'state': state,
            'zip_code': zip_code,
            'longitude': lon,
            'latitude': lat,
            'fire_data': address_data,
            'county_alerts': alerts
        }), 200