
#include "DHT.h"
#include <TinyGPS++.h>
#include <WiFi.h>
#include <PubSubClient.h>


const char* ssid = "Wokwi-GUEST";   
const char* password = "";          
const char* mqtt_server = "broker.hivemq.com";
const int mqtt_port = 1883;
const char* mqtt_topic = "esp32/dados";

#define TRIG_PIN 5
#define ECHO_PIN 18
#define LED_GREEN 2
#define LED_RED 4

WiFiClient espClient;
PubSubClient client(espClient);

unsigned long lastDetectAt = 0;
unsigned int motoCounter = 0;
const unsigned long DETECT_COOLDOWN_MS = 3000;
const int DISTANCE_THRESHOLD_CM = 40;

const char* ZONAS[] = {"ZC1", "ZC2", "ZE"};
const int ZONAS_COUNT = 3;

void setup_wifi() {
  Serial.print("Conectando ao Wi-Fi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWi-Fi conectado!");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());
}

void reconnect_mqtt() {
  while (!client.connected()) {
    Serial.print("Conectando ao MQTT...");
    if (client.connect("ESP32ClientMottu")) {
      Serial.println("Conectado!");
    } else {
      Serial.print("Falhou, rc=");
      Serial.print(client.state());
      Serial.println(" tentando em 5s...");
      delay(5000);
    }
  }
}

long measureDistanceCM() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH, 30000UL);
  if (duration == 0) return 9999;
  return duration / 58;
}

String randomZone() {
  return String(ZONAS[random(0, ZONAS_COUNT)]);
}

int randomVaga() {
  return random(1, 21);
}

void setup() {
  Serial.begin(115200);

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(LED_GREEN, OUTPUT);
  pinMode(LED_RED, OUTPUT);

  digitalWrite(LED_GREEN, LOW);
  digitalWrite(LED_RED, LOW);

  randomSeed(analogRead(34));

  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
}

void loop() {
  if (!client.connected()) {
    reconnect_mqtt();
  }
  client.loop();

  long dist = measureDistanceCM();
  unsigned long now = millis();

  if (dist > 0 && dist < DISTANCE_THRESHOLD_CM && (now - lastDetectAt) > DETECT_COOLDOWN_MS) {
    lastDetectAt = now;
    motoCounter++;

    String moto_id = "M" + String(motoCounter);
    String zona = randomZone();
    int vaga = randomVaga();

    bool entradaCorreta = (random(0, 100) < 70);

    String payload = "{";
    payload += "\"moto_id\":\"" + moto_id + "\",";
    payload += "\"zona\":\"" + zona + "\",";
    payload += "\"vaga\":" + String(vaga) + ",";
    payload += "\"status\":\"entrada\",";
    payload += "\"correct\":" + String(entradaCorreta ? "true" : "false") + ",";
    payload += "\"timestamp\":" + String(now);
    payload += "}";

    Serial.println("Publicando MQTT:");
    Serial.println(payload);
    client.publish(mqtt_topic, payload.c_str());

    if (entradaCorreta) {
      digitalWrite(LED_GREEN, HIGH);
      digitalWrite(LED_RED, LOW);
      delay(500);
      digitalWrite(LED_GREEN, LOW);
    } else {
      digitalWrite(LED_RED, HIGH);
      digitalWrite(LED_GREEN, LOW);
      delay(500);
      digitalWrite(LED_RED, LOW);
    }
  }

  delay(100);
}
