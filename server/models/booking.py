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

    def to_dict(self):
        return {
            "id": self.id,
            "user": self.user.to_dict(),           # ✅ user info
            "yacht": self.yacht.to_dict(),         # ✅ yacht info
            "start_date": str(self.start_date),
            "end_date": str(self.end_date),
            "total_price": self.total_price,
            "special_request": self.special_request,
            "addons": [a.to_dict() for a in self.addons]  # ✅ booking addons info
        }
