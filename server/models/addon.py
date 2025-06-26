from server.models.db import db
from sqlalchemy.orm import relationship

class AddOn(db.Model):
    __tablename__ = 'addons'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)

    bookings = relationship("BookingAddOn", back_populates="addon")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price
        }