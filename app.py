from app import create_app
from app.mqtt_client import start_mqtt

app = create_app()
start_mqtt()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
