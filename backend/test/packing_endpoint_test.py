import json


def test_get_packing_list_by_address_id(client):
    #create user
    user_data = { 
        'username': 'walter4',
        'password': 'password123',
        'confirm_password': 'password123',
        'email': 'wroth4@vols.utk.edu',
        'full_name': 'Walter Roth'
    }
    response = client.post('/users/', json=user_data)
    user_id = response.get_json()['user']['_id']

    #create address for user
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

    response = client.post(f'/addresses/user/{user_id}', json=address_data)
    address_id = response.get_json()['address']['_id']
    #take address id and get the packing list

    response = client.get(f'/packing/{address_id}')
    packing_list = response.get_json()['packing_list']
    assert response.status_code == 200 and packing_list != None

def test_update_packing_list(client):
    #create user
    user_data = { 
        'username': 'walter5',
        'password': 'password123',
        'confirm_password': 'password123',
        'email': 'wroth5@vols.utk.edu',
        'full_name': 'Walter Roth'
    }
    response = client.post('/users/', json=user_data)
    user_id = response.get_json()['user']['_id']

    #create address for user
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

    response = client.post(f'/addresses/user/{user_id}', json=address_data)
    address_id = response.get_json()['address']['_id']

    new_items = {
        'items': ['Food', 'Water', 'First Aid Kit']
    }

    response = client.put(f'/packing/{address_id}', json=new_items)
    assert response.status_code == 200 and 'previous_items' in response.get_json().keys() and 'new_items' in response.get_json().keys()

