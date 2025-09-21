from flask import Blueprint, render_template, jsonify
import json
import os

bp = Blueprint("main", __name__)
DATA_FILE = "data.json"  # caminho do seu arquivo de logs

@bp.route("/")
def dashboard():
    return render_template("index.html")

@bp.route("/logs")
def get_logs():
    if not os.path.exists(DATA_FILE):
        return jsonify([])

    with open(DATA_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []

    return jsonify(data)
