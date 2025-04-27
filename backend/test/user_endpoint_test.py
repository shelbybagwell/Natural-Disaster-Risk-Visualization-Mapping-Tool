import json

#ensure users below in the tests are not in the db prior to running to the test

def test_user_creation(client):

    user_data = { 
        'username': 'walter1',
        'password': 'password123',
        'confirm_password': 'password123',
        'email': 'wroth1@vols.utk.edu',
        'full_name': 'Walter Roth'
    }
    response = client.post('/users/', json=user_data)

    # Assert that a response code was transmitted from the endpoint 
    assert response.status_code == 201

def test_get_user_by_username(client):
    username = 'walter1'
    response = client.get(f'/users/{username}')
    res_username = response.get_json()['username']

    assert response.status_code == 200 and res_username == username

def test_get_user_by_user_id(client):

    user_data = { 
        'username': 'walter2',
        'password': 'password123',
        'confirm_password': 'password123',
        'email': 'wroth2@vols.utk.edu',
        'full_name': 'Walter Roth'
    }
    response = client.post('/users/', json=user_data)
    user_id = response.get_json()['user']['_id']

    response = client.get(f'/users/id/{user_id}')

    assert response.status_code == 200

def test_update_user_by_user_id(client):

    user_data = { 
        'username': 'walter3',
        'password': 'password123',
        'confirm_password': 'password123',
        'email': 'wroth3@vols.utk.edu',
        'full_name': 'Walter Roth'
    }
    response = client.post('/users/', json=user_data)
    user_id = response.get_json()['user']['_id']

    update_data = {
        'email': 'walterr3@vols.utk.edu'
    }

    response = client.put(f'/users/id/{user_id}', json=update_data)

    assert response.status_code == 200

