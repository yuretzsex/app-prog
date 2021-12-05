from flask import Blueprint, Response, request, jsonify
from marshmallow import ValidationError
from flask_bcrypt import Bcrypt
from models import User, Announcement, Local, Public, Session
from validation_schemas import user_schema, login_schema
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
import json

login = Blueprint('login', __name__)
user = Blueprint('user', __name__)
bcrypt = Bcrypt()
session = Session()


@user.route('/user', methods=['POST'])
def new_user():
    data = request.json

    try:
        user_schema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    exists = session.query(User).filter_by(username=data['username']).first()
    if exists:
        return Response(status=400, response='User with such username already exists.')

    exists = session.query(User).filter_by(phone=data['phone']).first()
    if exists:
        return Response(status=400, response='Phone was already taken')

    exists = session.query(User).filter_by(email=data['email']).first()
    if exists:
        return Response(status=400, response='This email was already taken')

    new_user = User(username=data['username'], firstName=data['firstName'], lastName=data['lastName'],
                    password=bcrypt.generate_password_hash(data['password']),
                    email=data['email'], phone=data['phone'], city=data['city'])

    session.add(new_user)
    session.commit()
    session.close()

    return Response(response='New user was successfully created!')


@user.route('/user/<userId>', methods=['GET'])
def get_user(userId):
    user_data = session.query(User).filter_by(id=userId).first()
    if not user_data:
        return Response(status=404, response='User was not found')

    user_data = {'id': user_data.id, 'username': user_data.username, 'firstName': user_data.firstName,
                 'lastName': user_data.lastName,
                 'email': user_data.email, 'phone': user_data.phone, 'city': user_data.city}
    return jsonify({"user": user_data})

@user.route('/user/<username>', methods=['GET'])
def get_user_byusername(username):
    user_data = session.query(User).filter_by(username=username).first()
    if not user_data:
        return Response(status=404, response='User was not found')

    user_data = {'id': user_data.id, 'username': user_data.username, 'firstName': user_data.firstName,
                 'lastName': user_data.lastName,
                 'email': user_data.email, 'phone': user_data.phone, 'city': user_data.city}
    return jsonify({"user": user_data})

@user.route('/user/<userId>', methods=['PUT'])
@jwt_required()
def update_user(userId):
    data = request.get_json(force=True)
    try:
        user_schema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    user_data = session.query(User).filter_by(id=userId).first()
    if not user_data:
        return Response(status=404, response='A user with provided ID was not found.')
    curr_user = get_jwt_identity()
    if curr_user != user_data.username:
        return Response(status=404, response="You are not allowed to do that")
    if 'username' in data.keys():
        exists = session.query(User).filter_by(username=data['username']).first()
        if exists:
            return Response(status=400, response='User with such username already exists.')
        user_data.username = data['username']
    if 'firstName' in data.keys():
        user_data.firstName = data['firstName']
    if "lastName" in data.keys():
        user_data.lastName = data['lastName']
    if 'password' in data.keys():
        hashed_password = bcrypt.generate_password_hash(data['password'])
        user_data.password = hashed_password
    if 'email' in data.keys():
        exists = session.query(User).filter_by(email=data['email']).first()
        if exists and exists.id != user_data.id:
            return Response(status=400, response='Email is already taken')
        user_data.email = data['email']
    if 'phone' in data.keys():
        exists = session.query(User).filter_by(phone=data['phone']).first()
        if exists and exists.id != user_data.id:
            return Response(status=400, response='Phone is already taken')
        user_data.phone = data['phone']
    if 'city' in data.keys():
        user_data.city = data['city']

    session.commit()
    session.close()
    access_token = create_access_token(identity=data['username'])
    return Response(f"Data was changed\nNew token:\n{access_token}")

@user.route('/user/<userId>', methods=['DELETE'])
@jwt_required()
def delete_user(userId):
    user_data = session.query(User).filter_by(id=userId).first()
    if not user_data:
        return Response(status=404, response="User does not exist")
    curr_user = get_jwt_identity()
    if curr_user != user_data.username:
        return Response(status=404, response="You are not allowed to do that")
    session.delete(user_data)
    session.commit()
    session.close()
    return Response(response='User was deleted')

@login.route('/login', methods=['GET'])
def logining():
    data = request.get_json(force=True)
    try:
        login_schema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    exist = session.query(User).filter_by(username=data['username']).first()
    access_token = create_access_token(identity=data['username'])
    if exist and bcrypt.check_password_hash(exist.password, data['password']):
            return jsonify({'access_token': access_token})
    else:
        return Response(status=404, response='Invalid username or password.')