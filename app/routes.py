from flask import Blueprint, render_template, jsonify
from sqlalchemy import text 

from .database import db_session, Telemetria

bp = Blueprint("main", __name__)

@bp.route("/")
def dashboard():
    """Serve a página principal do dashboard (o index.html)."""
    return render_template("index.html")

@bp.route("/logs")
def get_logs():
    """
    API para a TABELA DE LOGS e GRÁFICOS DE TENDÊNCIA.
    Retorna os 100 últimos eventos.
    """
    print("📡 [API] Pedido /logs recebido. A consultar o Oracle...")
    try:
        logs_recentes = Telemetria.query.order_by(Telemetria.timestamp.desc()).limit(100).all()
        logs_recentes.reverse()
        data_para_json = [log.to_dict() for log in logs_recentes]
        
        print(f"✅ [API] A enviar {len(data_para_json)} registos para o frontend.")
        return jsonify(data_para_json)

    except Exception as e:
        print(f"❌ [DB] Erro ao buscar logs: {e}")
        return jsonify({"error": "Erro interno ao consultar a base de dados"}), 500
    
    finally:
        db_session.remove()

@bp.route("/api/patio/status")
def get_patio_status():
    """
    API para o MAPA DO PÁTIO.
    Retorna o *estado atual* (quais vagas estão ocupadas).
    """
    print("📡 [API] Pedido /api/patio/status recebido. A calcular o estado do pátio...")
    try:
        query_sql = text("""
            WITH RankedLogs AS (
                SELECT
                    moto_id,
                    vaga,
                    status,
                    ROW_NUMBER() OVER(
                        PARTITION BY vaga 
                        ORDER BY timestamp DESC
                    ) as rn
                FROM
                    telemetria
                WHERE
                    vaga IS NOT NULL
            )
            SELECT
                moto_id,
                vaga
            FROM
                RankedLogs
            WHERE
                rn = 1
                AND status = 'entrada'
        """)
        
        result = db_session.execute(query_sql).mappings().all()
        
        vagas_ocupadas_lista = []
        for item in result:
            vagas_ocupadas_lista.append({
                "vaga": str(item.vaga), 
                "moto_id": item.moto_id
            })

        print(f"✅ [API] A enviar o estado de {len(vagas_ocupadas_lista)} vagas ocupadas.")
        
        return jsonify(vagas_ocupadas_lista)

    except Exception as e:
        print(f"❌ [DB] Erro ao calcular o estado do pátio: {e}")
        return jsonify({"error": "Erro interno ao calcular o estado do pátio"}), 500
    
    finally:
        db_session.remove()