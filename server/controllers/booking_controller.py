# server/controllers/booking_controller.py

from flask import Blueprint, request, jsonify
from server.models.booking import Booking
from server.models.db import db
from datetime import datetime

booking_bp = Blueprint('bookings', __name__, url_prefix='/bookings')

@booking_bp.route('/', methods=['GET'])
def get_bookings():
    bookings = Booking.query.all()
    return jsonify([booking.to_dict() for booking in bookings]), 200

@booking_bp.route('/', methods=['POST'])
def create_booking():
    data = request.get_json()
    try:
        new_booking = Booking(
            user_id=data['user_id'],
            yacht_id=data['yacht_id'],
            start_date=datetime.strptime(data['start_date'], "%Y-%m-%d"),
            end_date=datetime.strptime(data['end_date'], "%Y-%m-%d"),
            total_price=data.get('total_price'),
            special_request=data.get('special_request')
        )
        db.session.add(new_booking)
        db.session.commit()
        return jsonify(new_booking.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@booking_bp.route('/<int:id>', methods=['DELETE'])
def delete_booking(id):
    booking = Booking.query.get(id)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404
    db.session.delete(booking)
    db.session.commit()
    return jsonify({"message": "Booking deleted"}), 200
