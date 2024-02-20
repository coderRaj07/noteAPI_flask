from flask import jsonify, request
from flask_jwt_extended import create_access_token
from app.models.user import User

def signup():
    data = request.get_json()
    if not data or not data['username'] or not data['password']:
        return jsonify({'error': 'Username and password are required'}), 400
    if User.objects(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400

    user = User(username=data['username'], password=data['password']).save()
    return jsonify({'message': 'User created successfully'}), 201

def login():
    data = request.get_json()
    if not data or not data['username'] or not data['password']:
        return jsonify({'error': 'Username and password are required'}), 400

    user = User.objects(username=data['username'], password=data['password']).first()
    if not user:
        return jsonify({'error': 'Invalid username or password'}), 401
    print(user.id)
    access_token = create_access_token(identity=str(user.id))
    return jsonify(access_token=access_token), 200
