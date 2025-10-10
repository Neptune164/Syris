from flask import Flask,jsonify
import json


app = Flask(__name__)

@app.route("/predict", methods=["GET"])
def display():
    with open("result.json") as f:
        data = json.load(f)

    return jsonify(data)