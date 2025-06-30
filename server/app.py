# ✅ server/app.py

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import os

# Configuration + DB + Migrations
from server.config import Config
from server.models.db import db, migrate

# Blueprints (routes)
from server.controllers.yacht_controller import yacht_bp
from server.controllers.user_controller import user_bp
from server.controllers.booking_controller import booking_bp
from server.controllers.addon_controller import addon_bp
from server.controllers.auth_controller import auth_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ✅ Secret key for sessions (use .env in production)
    app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")

    # ✅ Database URI fallback (local PostgreSQL)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        'postgresql://maverick:pharaoh@localhost/yachtaway_db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ✅ Session config
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_SECURE'] = False  # Set True ONLY for HTTPS
    app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # Optional: 1 hour

    # ✅ Init session and database
    Session(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # ✅ CORS setup to allow React frontend (5173)
    CORS(
        app,
        origins=["http://localhost:5173"],
        supports_credentials=True  # 👈 must match Axios `withCredentials: true`
    )

    # ✅ Register all routes via Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(yacht_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(addon_bp)

    # ✅ Default route (test server)
    @app.route('/')
    def index():
        return {"message": "YachtAway API running ✅"}

    return app


# ✅ Create app instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
