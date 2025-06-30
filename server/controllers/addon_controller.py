# server/controllers/addon_controller.py

from flask import Blueprint, jsonify
from server.models.addon import AddOn

addon_bp = Blueprint('addons', __name__, url_prefix='/addons')

@addon_bp.route('/', methods=['GET'])
def get_addons():
    addons = AddOn.query.all()
    return jsonify([addon.to_dict() for addon in addons]), 200
