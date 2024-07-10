from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    '''
    Register new user endpoint

    Args:
      None

    Request:
      JSON object with username and password

    Action:
      Create a new user and save it to the database with hashed password

    Returns:
      str: JSON response
    '''
    data = request.get_json()
    hashed_password = generate_password_hash(
        data['password'], method='sha256')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Registered successfully'}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    '''
    Login user endpoint

    Args:
      None

    Request:
      JSON object with username and password

    Action:
      Check if the user exists and the password is correct
      Generate an access token and return it in a JSON response

    Returns:
      str: JSON response
    '''
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401
    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token}), 200
