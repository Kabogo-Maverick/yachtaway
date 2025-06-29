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

    # 🔗 Relationships
    user = relationship("User", back_populates="bookings")
    yacht = relationship("Yacht", back_populates="bookings")

    # Rename this relationship so it's clear it's BookingAddOn objects (not just AddOns)
    addon_links = relationship("BookingAddOn", back_populates="booking", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "user": self.user.to_dict(),           # ✅ include full user
            "yacht": self.yacht.to_dict(),         # ✅ include full yacht
            "start_date": self.start_date.strftime("%Y-%m-%d"),
            "end_date": self.end_date.strftime("%Y-%m-%d"),
            "total_price": self.total_price,
            "special_request": self.special_request,
            # ✅ return the actual add-ons, not the join table
            "addons": [ba.addon.to_dict() for ba in self.addon_links if ba.addon]
        }
