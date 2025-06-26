from flask import Blueprint, request, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from server.models.user import User
from server.models.db import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# -----------------------------
# POST /auth/signup
# -----------------------------
@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # Basic validations
    if not username or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    # Check for duplicate email
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already in use"}), 409

    # Create new user and hash password
    new_user = User(username=username, email=email)
    new_user.set_password(password)  # uses werkzeug hash method

    try:
        db.session.add(new_user)
        db.session.commit()

        # Log the user in
        session['user_id'] = new_user.id

        return jsonify(new_user.to_dict()), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------
# POST /auth/login
# -----------------------------
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        session['user_id'] = user.id
        return jsonify(user.to_dict()), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401


# -----------------------------
# DELETE /auth/logout
# -----------------------------
@auth_bp.route('/logout', methods=['DELETE'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logged out successfully"}), 200


# -----------------------------
# GET /auth/check_session
# -----------------------------
@auth_bp.route('/check_session', methods=['GET'])
def check_session():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        if user:
            return jsonify(user.to_dict()), 200
    return jsonify({"error": "Unauthorized"}), 401
