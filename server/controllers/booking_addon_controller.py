# server/controllers/booking_addon_controller.py

from flask import Blueprint, request, jsonify
from server.models.booking_addon import BookingAddOn
from server.models.db import db

booking_addon_bp = Blueprint('booking_addons', __name__, url_prefix='/booking-addons')

@booking_addon_bp.route('/', methods=['POST'])
def add_booking_addon():
    data = request.get_json()
    try:
        new_entry = BookingAddOn(
            booking_id=data['booking_id'],
            addon_id=data['addon_id'],
            quantity=data.get('quantity', 1)
        )
        db.session.add(new_entry)
        db.session.commit()
        return jsonify(new_entry.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@booking_addon_bp.route('/<int:booking_id>', methods=['GET'])
def get_addons_for_booking(booking_id):
    entries = BookingAddOn.query.filter_by(booking_id=booking_id).all()
    return jsonify([entry.to_dict() for entry in entries]), 200
