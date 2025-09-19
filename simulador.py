import json
import random
import time
import paho.mqtt.client as mqtt

MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "esp32/dados"

# Zonas novas
zonas = ["ZC1", "ZC2", "ZE"]

# Conecta no broker
client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

moto_counter = 1

try:
    while True:
        moto_id = f"M{moto_counter}"
        zona = random.choice(zonas)
        vaga = random.randint(1, 20)
        status = "entrada"
        correct = random.choice([True, False])
        timestamp = int(time.time())

        payload = {
            "moto_id": moto_id,
            "zona": zona,
            "vaga": vaga,
            "status": status,
            "correct": correct,
            "timestamp": timestamp
        }

        client.publish(MQTT_TOPIC, json.dumps(payload))
        print("📤 Published:", payload)

        moto_counter += 1
        time.sleep(2)  # publica a cada 2 segundos

except KeyboardInterrupt:
    client.loop_stop()
    print("Simulator stopped.")
