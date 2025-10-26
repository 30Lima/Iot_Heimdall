from flask import Blueprint, render_template, jsonify

# --- 1. Nossas importações da Base de Dados ---
# Importamos o "canal" (db_session) e o "mapa" (Telemetria)
from .database import db_session, Telemetria

bp = Blueprint("main", __name__)

@bp.route("/")
def dashboard():
    """Serve a página principal do dashboard (o index.html)."""
    return render_template("index.html")

@bp.route("/logs")
def get_logs():
    """
    Este é o endpoint da API que o seu JavaScript consome.
    Agora, ele busca os dados do Oracle.
    """
    print("📡 [API] Pedido /logs recebido. A consultar o Oracle...")
    try:
        # --- 2. A Consulta ao Oracle ---
        # Buscamos os 100 registos mais recentes.
        # .order_by(Telemetria.timestamp.desc()) -> Mais recentes primeiro
        # .limit(100) -> Pega apenas os 100 primeiros
        # .all() -> Executa a consulta
        logs_recentes = Telemetria.query.order_by(Telemetria.timestamp.desc()).limit(100).all()
        
        # Opcional: Inverte a lista para que fiquem em ordem cronológica (mais antigo primeiro)
        # O seu frontend (com .slice(-20)) provavelmente lida bem com qualquer ordem,
        # mas isto é mais "correto" para gráficos.
        logs_recentes.reverse()

        # --- 3. Conversão para JSON ---
        # Transformamos a lista de objetos [Telemetria, Telemetria, ...]
        # numa lista de dicionários [ {..}, {..}, ...] usando a função .to_dict()
        # que criámos no database.py.
        data_para_json = [log.to_dict() for log in logs_recentes]
        
        print(f"✅ [API] A enviar {len(data_para_json)} registos para o frontend.")
        return jsonify(data_para_json)

    except Exception as e:
        print(f"❌ [DB] Erro ao buscar logs: {e}")
        # Se o banco falhar, envia um erro 500 para o frontend
        return jsonify({"error": "Erro interno ao consultar a base de dados"}), 500
    
    finally:
        # --- 4. ESSENCIAL: Limpar a sessão ---
        # Assim como no mqtt_client, garantimos que cada pedido
        # (cada 2 segundos) devolve a ligação ao Oracle.
        db_session.remove()