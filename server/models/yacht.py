from server.models.db import db
from sqlalchemy.orm import relationship

class Yacht(db.Model):
    __tablename__ = 'yachts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(100))
    price_per_day = db.Column(db.Float, nullable=False)
    capacity = db.Column(db.Integer)
    image_url = db.Column(db.String)

    bookings = relationship("Booking", back_populates="yacht")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "location": self.location,
            "price_per_day": self.price_per_day,
            "capacity": self.capacity,
            "image_url": self.image_url
        }
