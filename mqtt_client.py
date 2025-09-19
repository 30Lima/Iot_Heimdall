import json
import threading
import paho.mqtt.client as mqtt

logs = []  # lista compartilhada com Flask

MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "esp32/dados"
DATA_FILE = "data.json"

def load_data():
    global logs
    try:
        with open(DATA_FILE, "r") as f:
            logs = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(logs, f, indent=4)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to MQTT Broker!")
        client.subscribe(MQTT_TOPIC)
    else:
        print("❌ Failed to connect, code:", rc)

def on_message(client, userdata, msg):
    global logs
    try:
        payload = msg.payload.decode()
        data = json.loads(payload)

        print("📥 Received:", data)

        logs.append(data)
        save_data()
    except Exception as e:
        print("⚠️ Error processing message:", e)

def start_mqtt():
    load_data()
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    # roda o loop MQTT em thread separada
    thread = threading.Thread(target=client.loop_forever)
    thread.daemon = True
    thread.start()
