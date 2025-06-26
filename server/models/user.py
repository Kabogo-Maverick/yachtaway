from sqlalchemy.orm import validates, relationship
from server.models.db import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)


    bookings = relationship('Booking', back_populates='user')
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }   

    def __repr__(self):
        return f'<User {self.username}>'
    

