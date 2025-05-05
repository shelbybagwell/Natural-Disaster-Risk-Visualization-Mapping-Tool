from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, set_refresh_cookies, unset_jwt_cookies
)

from helpers.user_helper import UserHelper

auth_blueprint = Blueprint('auth', __name__)

# User login
@auth_blueprint.route('/login', methods=['POST'])
def login():

    try: 

        data = request.json
        email = data.get('email')
        password = data.get('password')

        mongo = current_app.mongo
        users_collection = mongo.db.users

        if not email:
            raise Exception('Email is required.')
        
        if not password:
            raise Exception('Password is required.')

        User = users_collection.find_one({"email": email})

        if not User:
            raise Exception('An account with email address was not found. Please try again.')

        # Consider locking user account after X number of failed attempts?
        if not UserHelper.check_hashed_password(User['password'], password):
            raise Exception('The password you have entered in incorrect. Please try again.')

        access_token = create_access_token(
            identity=str(User['_id']),
            additional_claims={"email": User['email'], "role": "user"}
        )

        refresh_token = create_refresh_token(identity=email)

        response = jsonify({            
            "msg": "Login successful",
            "access_token" : access_token
        })
        
        set_refresh_cookies(response, refresh_token)
        return response

        # return jsonify({
        #     "msg": "Login successful",
        #     "access_token" : access_token, 
        #     "refresh_token" : refresh_token
        # }), 201

    except Exception as ex:
        return jsonify({"error": "%s" % ex}), 400
    
# User logout
@auth_blueprint.route('/logout', methods=['POST'])
def logout():

    try: 
        response = jsonify({"msg": "Logout successful"})
        unset_jwt_cookies(response)

        return response
    except Exception as ex:
        return jsonify({"error": "%s" % ex}), 400


@auth_blueprint.route('/refresh', methods=['POST'])
@jwt_required(refresh=True, locations=['cookies'])
def refresh():
    
    try: 
        identity = get_jwt_identity()
        new_access_token = create_access_token(identity=identity)
        response = jsonify(access_token=new_access_token)
        return response
    
    except Exception as ex:
        return jsonify({"error": "%s" % ex}), 400