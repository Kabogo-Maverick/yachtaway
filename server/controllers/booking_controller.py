# server/controllers/booking_controller.py

from flask import Blueprint, request, jsonify, session
from datetime import datetime
from server.models.booking import Booking
from server.models.db import db

booking_bp = Blueprint('bookings', __name__, url_prefix='/bookings')


@booking_bp.route('/my', methods=['GET'])
def get_my_bookings():
    print("🔐 [GET /bookings/my] Session:", session)
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    bookings = Booking.query.filter_by(user_id=user_id).all()
    return jsonify([b.to_dict() for b in bookings]), 200


@booking_bp.route('/', methods=['GET'])
def get_all_bookings():
    return jsonify([b.to_dict() for b in Booking.query.all()]), 200

# @booking_bp.route('/', methods=['POST'])  # 👈 No trailing slash to avoid CORS redirect bug
@booking_bp.route('', methods=['POST'])  # 👈 No trailing slash to avoid CORS redirect bug
def create_booking():
    print("🔐 [POST /bookings] Session:", session)
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        data = request.get_json()
        print("📥 Received booking data:", data)

        yacht_id = data.get('yacht_id')
        start_date = datetime.strptime(data.get('start_date'), "%Y-%m-%d")
        end_date = datetime.strptime(data.get('end_date'), "%Y-%m-%d")

        if not yacht_id or not start_date or not end_date:
            return jsonify({"error": "Missing required booking fields"}), 400

        if start_date >= end_date:
            return jsonify({"error": "End date must be after start date"}), 400

        # Check booking conflict
        conflict = Booking.query.filter(
            Booking.yacht_id == yacht_id,
            Booking.end_date > start_date,
            Booking.start_date < end_date
        ).first()

        if conflict:
            return jsonify({"error": "Yacht already booked during these dates"}), 409

        booking = Booking(
            user_id=user_id,
            yacht_id=yacht_id,
            start_date=start_date,
            end_date=end_date,
            total_price=data.get("total_price", 0),
            special_request=data.get("special_request", "")
        )

        db.session.add(booking)
        db.session.commit()

        print("✅ Booking created:", booking.to_dict())
        return jsonify(booking.to_dict()), 201

    except Exception as e:
        print("❌ Booking error:", str(e))
        return jsonify({"error": str(e)}), 400


@booking_bp.route('/<int:id>', methods=['DELETE'])
def delete_booking(id):
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    booking = Booking.query.get(id)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    db.session.delete(booking)
    db.session.commit()
    return jsonify({"message": "Booking deleted"}), 200
