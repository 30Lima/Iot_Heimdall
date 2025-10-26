import json
import threading
import paho.mqtt.client as mqtt

from .database import db_session, Telemetria

MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "esp32/dados"  

def on_connect(client, userdata, flags, rc):
    """Callback de conexão do MQTT."""
    if rc == 0:
        print("✅ [MQTT] Ligado com sucesso ao Broker!")
        client.subscribe(MQTT_TOPIC)
        print(f"🎧 [MQTT] Subscrito ao tópico: {MQTT_TOPIC}")
    else:
        print(f"❌ [MQTT] Falha ao ligar, código: {rc}")

def on_message(client, userdata, msg):
    """
    Callback de mensagem - O CORAÇÃO DO NOSSO BACKEND.
    Chamado sempre que o seu IoT envia dados.
    """
    try:
        payload = msg.payload.decode()
        data = json.loads(payload)
        print(f"📥 [MQTT] Mensagem recebida: {data}")

        nova_telemetria = Telemetria(
            moto_id = data.get('moto_id'),
            zona = data.get('zona'),
            vaga = data.get('vaga'),
            status = data.get('status'),
            correct = data.get('correct')
        )

        db_session.add(nova_telemetria)  
        db_session.commit()            
        
        print(f"💾 [DB] Dados salvos no Oracle para a moto: {nova_telemetria.moto_id}")

    except json.JSONDecodeError:
        print(f"⚠️ [MQTT] Erro: Mensagem recebida não é um JSON válido: {payload}")
    except Exception as e:
        print(f"❌ [DB] Erro ao salvar na base de dados: {e}")
        db_session.rollback()
    finally:
        db_session.remove()

def start_mqtt():
    """Inicia o cliente MQTT num thread separado."""
    
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1) 
    
    client.on_connect = on_connect
    client.on_message = on_message

    print(f"🔌 [MQTT] A tentar ligar ao broker: {MQTT_BROKER}...")
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    thread = threading.Thread(target=client.loop_forever)
    thread.daemon = True  
    thread.start()