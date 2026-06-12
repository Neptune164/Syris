from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

@app.route("/predict", methods=["GET", "POST", "OPTIONS"])
def display():
    filepath = os.path.join(os.path.dirname(__file__), "result.json")
    with open(filepath) as f:
        data = json.load(f)

    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=False)