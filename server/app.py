from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from server.models import User, Yacht, Booking, AddOn, BookingAddOn
import os
from server.config import Config
from server.models.db import db, migrate 


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)

    @app.route('/')
    def home():
        return {'message': 'Welcome to YachtAway API 🌊'}

    return app
