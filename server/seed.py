from server.app import create_app, db
from server.models import User, Yacht, AddOn
from werkzeug.security import generate_password_hash
from sqlalchemy import text  # ✅ Required for raw SQL
from datetime import datetime

app = create_app()

with app.app_context():
    print("🌱 Seeding database...")

    # Step 1: Clear old data (WRAPPED IN text())
    db.session.execute(text("DELETE FROM booking_addons"))
    db.session.execute(text("DELETE FROM bookings"))
    db.session.execute(text("DELETE FROM users"))
    db.session.execute(text("DELETE FROM yachts"))
    db.session.execute(text("DELETE FROM addons"))

    # Step 2: Reset auto-increment IDs (WRAPPED IN text())
    db.session.execute(text("ALTER SEQUENCE users_id_seq RESTART WITH 1"))
    db.session.execute(text("ALTER SEQUENCE yachts_id_seq RESTART WITH 1"))
    db.session.execute(text("ALTER SEQUENCE addons_id_seq RESTART WITH 1"))
    db.session.execute(text("ALTER SEQUENCE bookings_id_seq RESTART WITH 1"))
    db.session.execute(text("ALTER SEQUENCE booking_addons_id_seq RESTART WITH 1"))

    # Step 3: Create test users
    user1 = User(username="captainjoe", email="joe@yachtaway.com", password_hash=generate_password_hash("password123"))
    user2 = User(username="sailorjane", email="jane@yachtaway.com", password_hash=generate_password_hash("sailorpass"))

    # Step 4: Add yachts
    yacht1 = Yacht(name="Sea Breeze", description="Luxury yacht with sun deck and jacuzzi.", location="Mombasa", price_per_day=1500.00, capacity=8, image_url="https://example.com/seabreeze.jpg")
    yacht2 = Yacht(name="Ocean Pearl", description="Elegant yacht perfect for parties and weekend trips.", location="Diani", price_per_day=1200.00, capacity=6, image_url="https://example.com/oceanpearl.jpg")
    yacht3 = Yacht(name="Blue Lagoon", description="Modern yacht with AC and WiFi", location="Watamu", price_per_day=1900.00, capacity=10, image_url="https://example.com/bluelagoon.jpg")

    # Step 5: Add addons
    addon1 = AddOn(name="Private Chef", price=200.00)
    addon2 = AddOn(name="Fishing Gear", price=80.00)
    addon3 = AddOn(name="DJ", price=300.00)

    # Step 6: Commit
    db.session.add_all([user1, user2, yacht1, yacht2, yacht3, addon1, addon2, addon3])
    db.session.commit()

    print("✅ Done seeding!")
