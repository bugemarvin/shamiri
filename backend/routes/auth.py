from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from models.model import db, User, Profile

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
    user = User.query.filter_by(username=data['username']).first()
    if user:
        return jsonify({'message': 'user already exist'}), 409
    password = data['password']
    hashed_password = generate_password_hash(password)
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
    users = data['username']
    if '@' in users:
        user = Profile.query.filter_by(email=users).first()
    else:
        user = User.query.filter_by(username=users).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401
    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token}), 200


@auth_bp.route("/profile", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if request.method == 'PUT':
        data = request.get_json()
        if not data['email']:
            return jsonify({'message': 'please provide an email details'}), 409
        if not data['gender']:
            return jsonify({'message': 'please provide your gender details'}), 409
        if not data['phone_number']:
            return jsonify({'message': 'please provide a phone number'}), 409
        if not data['city']:
            return jsonify({'message': 'please provide your city detail'}), 409
        if not data['country']:
            return jsonify({'message': 'please provide your country detail'}), 409
        if not data['bio']:
            return jsonify({'message': 'please provide your bio data'}), 409
        if user.profile:
            user.profile.email = data['email']
            user.profile.gender = data['gender']
            user.profile.phone_number = data['phone_number']
            user.profile.city = data['city']
            user.profile.country = data['country']
            user.profile.bio = data['bio']
        else:
            new_profile = Profile(user_id=user_id, email=data['email'], gender=data['gender'],
                                  phone_number=data['phone_number'], city=data['city'], country=data['country'], bio=data['bio'])
            db.session.add(new_profile)
        db.session.commit()
        return jsonify({'message': 'Profile updated successfully'}), 200
    if request.method == 'GET':
        return jsonify({'username': user.username, 'email': user.profile.email if user.profile else '', 'gender': user.profile.gender if user.profile else '', 'phone_number': user.profile.phone_number if user.profile else '', 'city': user.profile.city if user.profile else '', 'country': user.profile.country if user.profile else '', 'bio': user.profile.bio if user.profile else ''}), 200
