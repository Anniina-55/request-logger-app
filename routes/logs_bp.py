from flask import Blueprint, jsonify
from collections import Counter
from utils.log_store import logs

logs_bp = Blueprint("logs", __name__)

@logs_bp.route("/api/logs", methods=["GET"])
def get_logs():
    return jsonify(logs)
