from flask import Blueprint, render_template, jsonify
import json
import os

bp = Blueprint("main", __name__)

# Caminho absoluto do arquivo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data.json")

@bp.route("/")
def dashboard():
    return render_template("index.html")

@bp.route("/logs")
def get_logs():
    # Lê o arquivo toda vez que o endpoint é acessado
    if not os.path.exists(DATA_FILE):
        return jsonify([])

    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        data = []

    return jsonify(data)
