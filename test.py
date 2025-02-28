from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

latest_gesture = ""  

@app.route('/')
def home():
    return "ESP8266 Data Receiver Running!"

@app.route('/data', methods=['POST'])
def receive_data():
    global latest_gesture
    data = request.get_data(as_text=True).strip()
    
    if data.startswith("DISTANCE:"):
        print(f"Received Distance Data: {data}")
    else:
        latest_gesture = data
        print(f"Received Gesture: {latest_gesture}")
    
    return jsonify({"message": "Data Received"}), 200

@app.route('/get_latest_gesture', methods=['GET'])
def get_latest_gesture():
    return jsonify({"gesture": latest_gesture})  

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
