from server.app import create_app, db
from server.models import User, Yacht, AddOn, Booking, BookingAddOn
from werkzeug.security import generate_password_hash
from sqlalchemy import text
from datetime import datetime

app = create_app()

with app.app_context():
    print("🌱 Seeding database...")

    # 1. Clear old data
    db.session.execute(text("DELETE FROM booking_addons"))
    db.session.execute(text("DELETE FROM bookings"))
    db.session.execute(text("DELETE FROM users"))
    db.session.execute(text("DELETE FROM yachts"))
    db.session.execute(text("DELETE FROM addons"))

    # 2. Reset sequences
    db.session.execute(text("ALTER SEQUENCE users_id_seq RESTART WITH 1"))
    db.session.execute(text("ALTER SEQUENCE yachts_id_seq RESTART WITH 1"))
    db.session.execute(text("ALTER SEQUENCE addons_id_seq RESTART WITH 1"))
    db.session.execute(text("ALTER SEQUENCE bookings_id_seq RESTART WITH 1"))
    db.session.execute(text("ALTER SEQUENCE booking_addons_id_seq RESTART WITH 1"))

    # 3. Users
    user1 = User(username="captainjoe", email="joe@yachtaway.com", password_hash=generate_password_hash("password123"))
    user2 = User(username="sailorjane", email="jane@yachtaway.com", password_hash=generate_password_hash("sailorpass"))

    # 4. Yachts
    yacht1 = Yacht(name="Sea Breeze", description="Luxury yacht with sun deck and jacuzzi.", location="Mombasa", price_per_day=1500.00, capacity=8, image_url="https://example.com/seabreeze.jpg")
    yacht2 = Yacht(name="Ocean Pearl", description="Elegant yacht perfect for parties and weekend trips.", location="Diani", price_per_day=1200.00, capacity=6, image_url="https://example.com/oceanpearl.jpg")
    yacht3 = Yacht(name="Blue Lagoon", description="Modern yacht with AC and WiFi", location="Watamu", price_per_day=1900.00, capacity=10, image_url="https://example.com/bluelagoon.jpg")

    # 5. Add-ons
    addon1 = AddOn(name="Private Chef", price=200.00)
    addon2 = AddOn(name="Fishing Gear", price=80.00)
    addon3 = AddOn(name="DJ", price=300.00)

    db.session.add_all([user1, user2, yacht1, yacht2, yacht3, addon1, addon2, addon3])
    db.session.commit()

    # 6. Bookings
    booking1 = Booking(
        user_id=user1.id,
        yacht_id=yacht1.id,
        start_date=datetime.strptime("2025-07-01", "%Y-%m-%d"),
        end_date=datetime.strptime("2025-07-05", "%Y-%m-%d"),
        total_price=6000.00,
        special_request="Anniversary setup"
    )

    booking2 = Booking(
        user_id=user2.id,
        yacht_id=yacht2.id,
        start_date=datetime.strptime("2025-07-10", "%Y-%m-%d"),
        end_date=datetime.strptime("2025-07-12", "%Y-%m-%d"),
        total_price=2400.00,
        special_request=None
    )

    db.session.add_all([booking1, booking2])
    db.session.commit()

    # 7. Booking AddOns
    ba1 = BookingAddOn(booking_id=booking1.id, addon_id=addon1.id, note="Vegetarian meals")
    ba2 = BookingAddOn(booking_id=booking1.id, addon_id=addon3.id, note="Bring Afrobeat playlist")
    ba3 = BookingAddOn(booking_id=booking2.id, addon_id=addon2.id, note="Kids-friendly gear")

    db.session.add_all([ba1, ba2, ba3])
    db.session.commit()

    print("✅ Done seeding!")
