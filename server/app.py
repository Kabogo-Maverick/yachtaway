from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from server.models import User, Yacht, Booking, AddOn, BookingAddOn
import os
from server.config import Config
from server.models.db import db, migrate 


from server.controllers.yacht_controller import yacht_bp
from server.controllers.user_controller import user_bp
from server.controllers.booking_controller import booking_bp
from server.controllers.addon_controller import addon_bp
from server.controllers.booking_addon_controller import booking_addon_bp
from server.controllers.auth_controller import auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, supports_credentials=True)
    db.init_app(app)
    migrate.init_app(app, db)

    @app.route('/')
    def home():
        return {'message': 'Welcome to YachtAway API 🌊'}

    #register blueprints
    app.register_blueprint(yacht_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(addon_bp)
    app.register_blueprint(booking_addon_bp)
    app.register_blueprint(auth_bp)



    return app

app = create_app()
