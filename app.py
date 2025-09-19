from flask import Flask
from routes import bp
from mqtt_client import start_mqtt

app = Flask(__name__)
app.register_blueprint(bp)

# Inicia o MQTT antes de rodar o Flask
start_mqtt()
    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
