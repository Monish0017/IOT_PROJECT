from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

latest_gesture = ""  # Store last received gesture

@app.route('/')
def home():
    return "ESP8266 Data Receiver Running!"

@app.route('/data', methods=['POST'])
def receive_data():
    global latest_gesture
    received_data = request.data.decode("utf-8").strip()

    if received_data:  # Update only if non-empty
        latest_gesture = received_data
    else:
        latest_gesture = ""  # Reset to empty string when no gesture

    print(f"Received Gesture: {latest_gesture}")
    return jsonify({"message": "Data Received"}), 200

@app.route('/get_latest_gesture', methods=['GET'])
def get_latest_gesture():
    return jsonify({"gesture": latest_gesture})  # Return latest received gesture as JSON

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
