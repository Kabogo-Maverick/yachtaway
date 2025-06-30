from flask import Blueprint, request, jsonify
from server.models.yacht import Yacht
from server.models.db import db

yacht_bp = Blueprint('yachts', __name__, url_prefix='/yachts')


@yacht_bp.route('/<int:id>', methods=['GET'])
def get_yacht_by_id(id):
    yacht = Yacht.query.get(id)
    if not yacht:
        return jsonify({"error": "Yacht not found"}), 404
    return jsonify(yacht.to_dict()), 200




@yacht_bp.route('/', methods=['GET'])
def get_all_yachts():
    yachts = Yacht.query.all()
    return jsonify([yacht.to_dict() for yacht in yachts]), 200

@yacht_bp.route('/', methods=['POST'])
def create_yacht():
    data = request.get_json()
    try:
        new_yacht = Yacht(
            name=data['name'],
            description=data.get('description'),
            location=data['location'],
            price_per_day=data['price_per_day'],
            capacity=data['capacity'],
            image_url=data.get('image_url')
        )
        db.session.add(new_yacht)
        db.session.commit()
        return jsonify(new_yacht.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
