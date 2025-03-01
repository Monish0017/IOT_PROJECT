from flask import Flask, jsonify
from flask_cors import CORS
import paho.mqtt.client as mqtt

app = Flask(__name__)
CORS(app)

MQTT_BROKER = "broker.emqx.io"
MQTT_PORT = 1883
MQTT_TOPIC = "iot/gesture"

latest_gesture = ""

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker!" if rc == 0 else "Connection failed!")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    global latest_gesture
    latest_gesture = msg.payload.decode("utf-8").strip()
    print(f"Received Gesture: {latest_gesture}")

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()

@app.route('/')
def home():
    return "ESP8266 MQTT Gesture Receiver Running!"

@app.route('/get_latest_gesture', methods=['GET'])
def get_latest_gesture():
    return jsonify({"gesture": latest_gesture})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
