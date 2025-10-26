from app import create_app
from app.mqtt_client import start_mqtt

app = create_app()

if __name__ == "__main__":
    start_mqtt() 

    app.run(debug=True, host="0.0.0.0", port=5000, use_reloader=False)