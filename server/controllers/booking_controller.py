from flask import Blueprint, request, jsonify, session
from server.models.booking import Booking
from server.models.db import db
from datetime import datetime

booking_bp = Blueprint('bookings', __name__, url_prefix='/bookings')

# GET /bookings/my - Only current user's bookings
@booking_bp.route('/my', methods=['GET'])
def get_my_bookings():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    bookings = Booking.query.filter_by(user_id=user_id).all()
    return jsonify([b.to_dict() for b in bookings]), 200

# GET /bookings - Admin view (optional)
@booking_bp.route('/', methods=['GET'])
def get_all_bookings():
    bookings = Booking.query.all()
    return jsonify([booking.to_dict() for booking in bookings]), 200

# POST /bookings - Create new booking
@booking_bp.route('/', methods=['POST'])
def create_booking():
    if not session.get('user_id'):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    try:
        user_id = session['user_id']
        yacht_id = data['yacht_id']
        start_date = datetime.strptime(data['start_date'], "%Y-%m-%d")
        end_date = datetime.strptime(data['end_date'], "%Y-%m-%d")

        if start_date >= end_date:
            return jsonify({"error": "End date must be after start date"}), 400

        # Check for overlapping bookings for same yacht
        conflict = Booking.query.filter(
            Booking.yacht_id == yacht_id,
            Booking.end_date > start_date,
            Booking.start_date < end_date
        ).first()
        if conflict:
            return jsonify({"error": "Yacht already booked during these dates"}), 409

        new_booking = Booking(
            user_id=user_id,
            yacht_id=yacht_id,
            start_date=start_date,
            end_date=end_date,
            total_price=data.get('total_price'),
            special_request=data.get('special_request')
        )

        db.session.add(new_booking)
        db.session.commit()
        return jsonify(new_booking.to_dict()), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# DELETE /bookings/<id> - Delete only if logged in
@booking_bp.route('/<int:id>', methods=['DELETE'])
def delete_booking(id):
    if not session.get('user_id'):
        return jsonify({"error": "Unauthorized"}), 401

    booking = Booking.query.get(id)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    db.session.delete(booking)
    db.session.commit()
    return jsonify({"message": "Booking deleted"}), 200
