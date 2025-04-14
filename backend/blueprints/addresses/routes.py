from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
from bson.objectid import ObjectId
from helpers.address_helper import AddressHelper
from geopy.geocoders import Nominatim

# #configuration for imports
import sys, os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.append(project_root)

from data.FIRMS_API import FIRMS_API_Client
from data.NOAA_API import NOAA_API_Client



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
    

@addresses_blueprint.route('/search', methods=['GET', 'POST'])
def search():
    match request.method:
        case 'GET': #this can be substituted for the angular front end was just using this as a placeholder and testing
            return f'''
                <h3>Enter your address: </h1>
                <form method="post" action="/addresses/search">
                    <input type="text" name="street_address" placeholder="Street Address" required /><br>
                    <input type="text" name="address_line2" placeholder="Address Line 2 (optional)" /><br>
                    <input type="text" name="city" placeholder="City" required /><br>
                    <input type="text" name="state" placeholder="State" required /><br>
                    <input type="text" name="zip" placeholder="ZIP Code" required /><br>
                    <button type="submit">Submit</button>
                </form>
            '''
        case 'POST': #example of posting user input to backend and making a call to the api and returning data/alerts for that address
            #201 W Washington Blvd, Los Angeles, CA 90007 (Mcdonalds)
            
            #get form data
            street_address = request.form.get('street_address')
            address_line2 = request.form.get('address_line2')
            city = request.form.get('city')
            state = request.form.get('state')
            zip_code = request.form.get('zip')

            #geopy the address to get lon/lat
            strAddress = street_address + ', ' + city + ', ' + state + ' ' + zip_code
            geolocator = Nominatim(user_agent='user_address')
            location = geolocator.geocode(strAddress)
            lon = location.longitude
            lat = location.latitude

            #add db insert/check here for user if logged in

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
                    county = c.strip().lower()
            
            county_codes = []
            for z in zones:
                if county in z['name'].lower():
                    county_codes.append(z)

            alerts = []
            for c in county_codes:
                data = n.get_alerts_for_zone(c['zone_id'])
                data['name'] = c['name']
                alerts.append(data)

            user_query = request.form.get('query')
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
            })