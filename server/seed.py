from server.app import create_app, db
from server.models import User, Yacht, AddOn
from datetime import datetime

app = create_app()

with app.app_context():
    print("🌱 Seeding database...")

    # Clear existing data
    User.query.delete()
    Yacht.query.delete()
    AddOn.query.delete()

    # Create Users
    user1 = User(username="captainjoe", email="joe@yachtaway.com", password_hash="hashed123")
    user2 = User(username="sailorjane", email="jane@yachtaway.com", password_hash="hashed456")

    # Create Yachts
    yacht1 = Yacht(
        name="Sea Breeze",
        description="Luxury yacht with sun deck and jacuzzi.",
        location="Mombasa",
        price_per_day=1500.00,
        capacity=8,
        image_url="https://example.com/seabreeze.jpg"
    )
    yacht2 = Yacht(
        name="Ocean Pearl",
        description="Elegant yacht perfect for parties and weekend trips.",
        location="Diani",
        price_per_day=1200.00,
        capacity=6,
        image_url="https://example.com/oceanpearl.jpg"
    )

    # Create AddOns
    addon1 = AddOn(name="Private Chef", price=200.00)
    addon2 = AddOn(name="Fishing Gear", price=80.00)
    addon3 = AddOn(name="DJ", price=300.00)

    # Add to session and commit
    db.session.add_all([user1, user2, yacht1, yacht2, addon1, addon2, addon3])
    db.session.commit()

    print("✅ Done seeding!")
