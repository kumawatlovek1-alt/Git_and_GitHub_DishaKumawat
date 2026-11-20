
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api")
def get_data():
    import json

    with open("data.json", "r") as file:
        data = json.load(file)

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
