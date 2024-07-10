from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
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
