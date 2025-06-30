from flask import Blueprint, request, jsonify
from server.models.user import User
from server.models.db import db
from werkzeug.security import generate_password_hash  # ✅ ADD THIS

user_bp = Blueprint('users', __name__, url_prefix='/users')

@user_bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

# @user_bp.route('/', methods=['GET'])
# def get_user_by_id()


@user_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    try:
        hashed_password = generate_password_hash(data['password'])  # ✅ HASHING HERE
        new_user = User(
            username=data['username'],
            email=data['email'],
            password_hash=hashed_password  # ✅ SECURE PASSWORD STORAGE
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
