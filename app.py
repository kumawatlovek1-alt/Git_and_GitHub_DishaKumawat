
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import certifi

load_dotenv()

app = Flask(__name__)

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(
    MONGO_URI,
    tlsCAFile=certifi.where()
)

db = client["TodoDB"]
collection = db["todo"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api")
def get_data():
    import json

    with open("data.json", "r") as file:
        data = json.load(file)

    return jsonify(data)

@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    item_name = request.form.get("itemName")
    item_description = request.form.get("itemDescription")

    todo = {
        "itemName": item_name,
        "itemDescription": item_description
    }

    result = collection.insert_one(todo)

    return jsonify({
        "item_id": str(result.inserted_id),
        "message": "Item submitted successfully!"
    })

if __name__ == "__main__":
    app.run(debug=True)
