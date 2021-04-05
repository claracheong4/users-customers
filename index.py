import os

from flask import Flask, request
from flask_cors import CORS

import hashlib

import authModel
import customerModel

app = Flask(__name__)

CORS(app)

# POST: Add user
@app.route('/user', methods=['POST'])
def add_user():
    id = request.args.get('id', None)
    secret = request.args.get('secret', None)

    hash_object = hashlib.sha1(bytes(secret, 'utf-8'))
    hashed_client_secret = hash_object.hexdigest()

    result = authModel.addUser(id, hashed_client_secret)

    if result == False:
        return {'success': False}
    else:
        return {'success': True}

# POST: Authenticate user
@app.route('/auth', methods=['POST'])
def auth():
    id = request.args.get('id', None)
    secret = request.args.get('secret', None)

    hash_object = hashlib.sha1(bytes(secret, 'utf-8'))
    hashed_client_secret = hash_object.hexdigest()

    result = authModel.authenticate(id, hashed_client_secret)

    if result == False:
        return {'success': False}
    else:
        return result

# POST: Verify user
@app.route('/verify', methods=['POST'])
def verify():
    authorizationHeader = request.headers.get('authorization')
    if not authorizationHeader:
        return {'success': False, 'message': 'No token provided.'}
    token = authorizationHeader.replace("Bearer ","")

    result = authModel.verify(token)

    if result:
        return {'success': True}
    else:
        return {'success': False}

# POST: Logout user
@app.route('/logout', methods=['POST'])
def logout_user():
    token = request.args.get("token")

    result = authModel.blacklist(token)

    if result == False:
        return {'success': False}
    else:
        return {'success': True}

# GET: Fetch all customers
@app.route('/customers')
def fetch_all_customers():
    authorizationHeader = request.headers.get('authorization')
    if not authorizationHeader:
        return {'success': False, 'message': 'No token provided.'}
    token = authorizationHeader.replace("Bearer ","")

    verification = authModel.verify(token)

    if verification == False:
        return {'success': False, 'message': 'Access Denied'}

    result = customerModel.fetchAll()

    if result == False:
        return {'success': False}
    else:
        return result

# DELETE: Reset customers table
@app.route('/customers', methods=['DELETE'])
def reset_customers():
    authorizationHeader = request.headers.get('authorization')
    if not authorizationHeader:
        return {'success': False, 'message': 'No token provided.'}
    token = authorizationHeader.replace("Bearer ","")

    verification = authModel.verify(token)

    if verification == False:
        return {'success': False, 'message': 'Access Denied'}

    result = customerModel.deleteAll()

    if result == False:
        return {'success': False}
    else:
        return {'success': True}

# POST: Add customer
@app.route('/customer', methods=['POST'])
def add_customer():
    authorizationHeader = request.headers.get('authorization')
    if not authorizationHeader:
        return {'success': False, 'message': 'No token provided.'}
    token = authorizationHeader.replace("Bearer ","")

    verification = authModel.verify(token)

    if verification == False:
        return {'success': False, 'message': 'Access Denied'}

    id = request.args.get('id', None)
    name = request.args.get('name', None)
    dob = request.args.get('dob', None)

    result = customerModel.add(id, name, dob)

    if result == False:
        return {'success': False}
    else:
        return result

# PUT: Update customer
@app.route('/customer', methods=['PUT'])
def update_customer():
    authorizationHeader = request.headers.get('authorization')
    if not authorizationHeader:
        return {'success': False, 'message': 'No token provided.'}
    token = authorizationHeader.replace("Bearer ","")

    verification = authModel.verify(token)

    if verification == False:
        return {'success': False, 'message': 'Access Denied'}

    id = request.args.get('id', None)
    name = request.args.get('name', None)
    dob = request.args.get('dob', None)

    result = customerModel.update(id, name, dob)

    if result == False:
        return {'success': False}
    else:
        return result

# DELETE: Delete customer
@app.route('/customer', methods=['DELETE'])
def delete_customer():
    authorizationHeader = request.headers.get('authorization')
    if not authorizationHeader:
        return {'success': False, 'message': 'No token provided.'}
    token = authorizationHeader.replace("Bearer ","")

    verification = authModel.verify(token)

    if verification == False:
        return {'success': False, 'message': 'Access Denied'}

    id = request.args.get('id', None)

    result = customerModel.delete(id)

    if result == False:
        return {'success': False}
    else:
        return {'success': True}

# GET: Get n youngest customers
@app.route('/customers/dob')
def get_youngest_customers():
    authorizationHeader = request.headers.get('authorization')
    if not authorizationHeader:
        return {'success': False, 'message': 'No token provided.'}
    token = authorizationHeader.replace("Bearer ","")

    verification = authModel.verify(token)

    if verification == False:
        return {'success': False, 'message': 'Access Denied'}

    n = request.args.get('n', None)

    result = customerModel.fetch_youngest_customers(n)

    if result == False:
        return {'success': False}
    else:
        return result

if __name__ == "__main__":
    app.run(debug=True)
