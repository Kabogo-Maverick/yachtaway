from server.models.db import db
from sqlalchemy.orm import relationship

class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    yacht_id = db.Column(db.Integer, db.ForeignKey('yachts.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    total_price = db.Column(db.Float)
    special_request = db.Column(db.String)

    user = relationship("User", back_populates="bookings")
    yacht = relationship("Yacht", back_populates="bookings")
    addons = relationship("BookingAddOn", back_populates="booking")
