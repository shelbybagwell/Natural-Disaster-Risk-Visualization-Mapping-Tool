from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from config import Config
from geopy.geocoders import Nominatim

#configuration for imports
import sys, os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

#api class imports
from data.NOAA_API import NOAA_API_Client
from data.ESRI_API import ESRI_API_Client
from data.FEMA_API import FEMA_API_Client
from data.FIRMS_API import FIRMS_API_Client
from data.NRI_API import NRI_API_Client




app = Flask(__name__)
app.config.from_object(Config)

mongo = PyMongo(app)  # Initialize MongoDB connection

@app.route('/')
def home():
    return jsonify({"message": "Flask connected to MongoDB!"})

@app.route('/test')
def get_data():
    collection = mongo.db.test_collection
    data = list(collection.find({}, {"_id": 0}))  # Exclude MongoDB ObjectId
    return jsonify(data)


@app.route('/search', methods=['GET', 'POST'])
def search():
    match request.method:
        case 'GET': #this can be substituted for the angular front end was just using this as a placeholder and testing
            return f'''
                <h3>Enter your address: </h1>
                <form method="post" action="/search">
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
    
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)