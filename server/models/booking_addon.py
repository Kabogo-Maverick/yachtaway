from server.models.db import db
from sqlalchemy.orm import relationship

class BookingAddOn(db.Model):
    __tablename__ = 'booking_addons'

    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    addon_id = db.Column(db.Integer, db.ForeignKey('addons.id'), nullable=False)
    note = db.Column(db.String)

    booking = relationship("Booking", back_populates="addons")
    addon = relationship("AddOn", back_populates="bookings")

    def to_dict(self):
        return {
            "id": self.id,
            "booking_id": self.booking_id,
            "note": self.note,
            "addon": self.addon.to_dict()  # ✅ Return full addon info
        }
