import json

# http://localhost:5000/addresses/user/67fa6b2e8f9c7fa7945e833c
def test_is_address_endpoint_reachable(client):

    address_data = {}
    response = client.post("/addresses/user/67fa6b2e8f9c7fa7945e833c", json=address_data)

    # Assert that a response code was transmitted from the endpoint 
    assert response.status_code != None


def test_is_invalid_address_rejected(client):

    # Test 1: Data with missing fields - (city is missing)
    address_data = {
        "street_1" : "", 
        "street_2" : "", 
        "state" : "", 
        "zip" : "", 
        "country" : "", 
        "address_name" : "", 
        "is_primary" : "0"
    }

    response = client.post("/addresses/user/67fa6b2e8f9c7fa7945e833c", json=address_data)
    assert response.status_code == 400

    # Expected error is city field is missing in request
    error = response.get_json().get("error", "")
    assert error == "Whoops: city field is required"


    # Test 2: Invalid data - zip is invalid
    address_data = {
        "street_1" : "201 W Washington Blvd", 
        "street_2" : "", 
        "city" : "Los Angeles", 
        "state" : "CA", 
        "zip" : "whoops", 
        "country" : "USA", 
        "address_name" : "McDonalds", 
        "is_primary" : "0"
    }

    response = client.post("/addresses/user/67fa6b2e8f9c7fa7945e833c", json=address_data)
    assert response.status_code == 400

    # Expected error for invalid zip codes
    error = response.get_json().get("error", "")
    assert error == "Please provide a valid zip code"

    # Test 3: Valid data, but non-existent address (should be rejected by GeoCode check) 
    address_data = {
        "street_1" : "123 Easy Street", 
        "street_2" : "", 
        "city" : "Fake City", 
        "state" : "CA", 
        "zip" : "12345", 
        "country" : "USA", 
        "address_name" : "Fake City Test", 
        "is_primary" : "0"
    }

    response = client.post("/addresses/user/67fa6b2e8f9c7fa7945e833c", json=address_data)
    assert response.status_code == 400

    # Expected error for invalid addresses
    error = response.get_json().get("error", "")
    assert error == "Unable to verify this address"


def test_create_address_success(client):

    # Verified/valid address
    address_data = {
        "street_1" : "201 W Washington Blvd", 
        "street_2" : "", 
        "city" : "Los Angeles", 
        "state" : "CA", 
        "zip" : "90007", 
        "country" : "USA", 
        "address_name" : "McDonalds", 
        "is_primary" : "0"
    }

    # Successful response should return HTTP code 201
    response = client.post("/addresses/user/67fa6b2e8f9c7fa7945e833c", json=address_data)
    assert response.status_code == 201

    # Expected success message
    message = response.get_json().get("message", "")
    assert message == "Address created successfully"

    # Ensure the address object is returned
    address = response.get_json().get("address", "")
    assert address != None

    # Ensure the address object has an "_id" field populated by MongoDB and is not null
    assert "_id" in address
    assert address["_id"] != None
    