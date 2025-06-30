from flask import Blueprint, request, jsonify, session
from datetime import datetime
from server.models.booking import Booking
from server.models.booking_addon import BookingAddOn
from server.models.addon import AddOn
from server.models.db import db

booking_bp = Blueprint('bookings', __name__, url_prefix='/bookings')


# ✅ Get bookings for the logged-in user
@booking_bp.route('/my', methods=['GET'])
def get_my_bookings():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    bookings = Booking.query.filter_by(user_id=user_id).all()
    return jsonify([b.to_dict() for b in bookings]), 200


# ✅ Create new booking
@booking_bp.route('', methods=['POST'])
def create_booking():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        data = request.get_json()
        yacht_id = data.get('yacht_id')
        start_date = datetime.strptime(data.get('start_date'), "%Y-%m-%d")
        end_date = datetime.strptime(data.get('end_date'), "%Y-%m-%d")
        total_price = data.get('total_price')
        special_request = data.get('special_request', "")
        addon_ids = data.get('addon_ids', [])

        if start_date >= end_date:
            return jsonify({"error": "End date must be after start date"}), 400

        booking = Booking(
            user_id=user_id,
            yacht_id=yacht_id,
            start_date=start_date,
            end_date=end_date,
            total_price=total_price,
            special_request=special_request
        )
        db.session.add(booking)
        db.session.commit()

        for addon_id in addon_ids:
            db.session.add(BookingAddOn(booking_id=booking.id, addon_id=addon_id))

        db.session.commit()
        return jsonify(booking.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Booking creation failed: {str(e)}"}), 400


# ✅ Update existing booking
@booking_bp.route('/<int:id>', methods=['PUT'])
def update_booking(id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    booking = Booking.query.get(id)
    if not booking or booking.user_id != user_id:
        return jsonify({"error": "Booking not found or unauthorized"}), 404

    try:
        data = request.get_json()

        # ✅ STEP 3 — Fallback for missing yacht_id
        yacht_id = data.get('yacht_id', booking.yacht_id)
        if not yacht_id:
            return jsonify({"error": "Missing yacht_id"}), 400
        booking.yacht_id = yacht_id

        # Update date and price
        start_date = datetime.strptime(data.get('start_date'), "%Y-%m-%d")
        end_date = datetime.strptime(data.get('end_date'), "%Y-%m-%d")
        if start_date >= end_date:
            return jsonify({"error": "End date must be after start date"}), 400

        booking.start_date = start_date
        booking.end_date = end_date
        booking.total_price = data.get('total_price')
        booking.special_request = data.get('special_request', "")

        # ✅ STEP 4 — Validate and update add-ons
        addon_ids = data.get('addon_ids', [])
        BookingAddOn.query.filter_by(booking_id=booking.id).delete()

        for addon_id in addon_ids:
            if not AddOn.query.get(addon_id):
                return jsonify({"error": f"Addon {addon_id} not found"}), 400
            db.session.add(BookingAddOn(booking_id=booking.id, addon_id=addon_id))

        db.session.commit()
        return jsonify(booking.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Booking update failed: {str(e)}"}), 400


# ✅ Delete booking
@booking_bp.route('/<int:id>', methods=['DELETE'])
def delete_booking(id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    booking = Booking.query.get(id)
    if not booking or booking.user_id != user_id:
        return jsonify({"error": "Booking not found or unauthorized"}), 404

    db.session.delete(booking)
    db.session.commit()
    return jsonify({"message": "Booking deleted"}), 200
