from flask import Blueprint, render_template, jsonify
from mqtt_client import logs  # importa a lista compartilhada

bp = Blueprint("main", __name__)

@bp.route("/")
def dashboard():
    return render_template("index.html")

@bp.route("/logs")
def get_logs():
    # retorna os logs em tempo real
    return jsonify(logs)
