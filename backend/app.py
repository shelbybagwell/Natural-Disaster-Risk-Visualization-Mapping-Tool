from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from config import Config

#configuration for imports
import sys, os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

#api class imports
from data.NOAA_API import NOAA_API_Client




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
                <h2>Enter your zip: </h2>
                <form method="post" action="/search">
                    <input type="text" name="query" placeholder="Type something..." />
                    <button type="submit">Search</button>
                    <p></p>
                </form>
            '''
        case 'POST': #example of posting user input to backend and making a call to the api and returning data/alerts for that address
            n = NOAA_API_Client()
            ca = n.get_state_zone_ids(state='CA')
            south_ca_ids = []
            south_ca_counties = ['imperial', 'kern', 'los angeles', 'orange', 'riverside', 'san bernardino', 'san diego', 'san luis obispo', 'santa barbara', 'ventura']

            for c in ca: 
                for s in south_ca_counties:
                    if s in c[1]['name'].lower():
                        south_ca_ids.append(c[0])
        
            alerts = []
            for i in south_ca_ids:
                print('Checking: ', i)
                alerts.append(n.get_alerts_for_zone(i))

            user_query = request.form.get('query')
            return jsonify({'response': alerts})
    
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)