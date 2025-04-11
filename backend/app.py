from flask import Flask, jsonify
from flask_pymongo import PyMongo
from config import Config

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)