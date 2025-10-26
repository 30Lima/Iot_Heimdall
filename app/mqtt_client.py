import json
import threading
import paho.mqtt.client as mqtt

# --- 1. Nossas importações da Base de Dados ---
# Importamos o "canal" (db_session) e o "mapa" (Telemetria)
from .database import db_session, Telemetria

# --- 2. Configuração do MQTT (sem alterações) ---
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "esp32/dados"  # O seu ESP32 deve publicar neste tópico

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
        # 1. Receber e descodificar a mensagem do IoT
        payload = msg.payload.decode()
        data = json.loads(payload)
        print(f"📥 [MQTT] Mensagem recebida: {data}")

        # 2. Mapear o JSON para o nosso "mapa" da tabela (Telemetria)
        # Usamos .get() para evitar erros se uma chave não existir no JSON
        nova_telemetria = Telemetria(
            moto_id = data.get('moto_id'),
            zona = data.get('zona'),
            vaga = data.get('vaga'),
            status = data.get('status'),
            correct = data.get('correct')
            # Nota: O 'id' (autoincrement) e 'timestamp' (default)
            # são geridos automaticamente pela base de dados.
        )

        # 3. Salvar na base de dados
        db_session.add(nova_telemetria)  # Adiciona à "fila"
        db_session.commit()             # Envia para o Oracle
        
        print(f"💾 [DB] Dados salvos no Oracle para a moto: {nova_telemetria.moto_id}")

    except json.JSONDecodeError:
        print(f"⚠️ [MQTT] Erro: Mensagem recebida não é um JSON válido: {payload}")
    except Exception as e:
        print(f"❌ [DB] Erro ao salvar na base de dados: {e}")
        # Se algo falhar (ex: Oracle offline), desfazemos a transação
        db_session.rollback()
    finally:
        # 4. ESSENCIAL: Limpar a sessão
        # Isto é crucial num script que corre para sempre (como este thread).
        # Fecha a ligação e devolve-a à "pool" de ligações.
        db_session.remove()

def start_mqtt():
    """Inicia o cliente MQTT num thread separado."""
    
    # Nota: paho-mqtt v2+ (que instalámos) exige esta linha
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1) 
    
    client.on_connect = on_connect
    client.on_message = on_message

    print(f"🔌 [MQTT] A tentar ligar ao broker: {MQTT_BROKER}...")
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    # Inicia o loop do MQTT num thread de background
    thread = threading.Thread(target=client.loop_forever)
    thread.daemon = True  # Permite que o programa feche mesmo com este thread a correr
    thread.start()