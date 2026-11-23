
from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
from pymongo import MongoClient
import os
import certifi
import json

load_dotenv()

app = Flask(__name__)

# MongoDB Atlas Connection
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("MONGO_URI not found in .env file")

client = MongoClient(
    MONGO_URI,
    tlsCAFile=certifi.where()
)

db = client["todo_db"]
todo_collection = db["todo_items"]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api")
def get_data():
    with open("data.json", "r") as file:
        data = json.load(file)

    return jsonify(data)


@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    item_name = request.form.get("itemName")
    item_description = request.form.get("itemDescription")

    if not item_name or not item_description:
        return jsonify({"error": "Both fields are required"}), 400

    todo_item = {
        "itemName": item_name,
        "itemDescription": item_description
    }

    result = todo_collection.insert_one(todo_item)

    return jsonify({
    "message": "Item submitted successfully!",
    "item_id": str(result.inserted_id)
}), 201

if __name__ == "__main__":
    app.run(debug=True)
