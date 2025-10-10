from flask import Flask

app = Flask(__name__)

@app.route("/predict", methods=["GET"])
def display():
    result = {
        "status": "successful"
    }
    return result