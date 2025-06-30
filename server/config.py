import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f"postgresql://maverick:pharaoh@localhost:5432/yachtaway_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSONIFY_PRETTYPRINT_REGULAR = True
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
