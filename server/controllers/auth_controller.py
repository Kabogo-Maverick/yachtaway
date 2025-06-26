from flask import Blueprint, request, session, jsonify
from server.models.user import User
from server.models.db import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# POST /auth/signup
@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    try:
        new_user = User(
            username=data['username'],
            email=data['email']
        )
        new_user.set_password(data['password'])

        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.id  # login user automatically

        return jsonify(new_user.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# POST /auth/login
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get("username")).first()

    if user and user.check_password(data.get("password")):
        session['user_id'] = user.id
        return jsonify(user.to_dict()), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401

# GET /auth/logout
@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logged out"}), 200

# GET /auth/check_session
@auth_bp.route('/check_session', methods=['GET'])
def check_session():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        return jsonify(user.to_dict()), 200
    return jsonify({"error": "Unauthorized"}), 401
