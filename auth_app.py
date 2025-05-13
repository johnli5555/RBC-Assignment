import os
from flask import Flask, request, jsonify, session, render_template
from flask_cors import CORS
from dotenv import load_dotenv

from backend.alter_client_field import alter_client_field
from backend.retrieve_client import retrieve_client_details

# Load env variables
load_dotenv()

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "super-secret-fallback-key")  # for sessions


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    client_id = data.get("client_id")
    password = data.get("password")

    # Check if both fields are provided
    if client_id is None or not password:
        return jsonify({"error": "Client ID and password are required."}), 400
    
    data = retrieve_client_details(client_id)

    # If retrieval failed (string returned instead of dict), handle as error
    if isinstance(data, str):
        return jsonify({"error": data}), 404

    # Validate password
    if data.get("password") != password:
            return jsonify({"error": "Invalid credentials."}), 401

    # Store session state
    session["client_id"] = client_id
    return jsonify({"message": "Login successful."})



@app.route("/update_password", methods=["POST"])
def update_password():
    if "client_id" not in session:
        return jsonify({"error": "Unauthorized. Please log in first."}), 403

    # Get new password from request
    data = request.get_json()
    new_password = data.get("new_password")
    if not new_password:
        return jsonify({"error": "New password required."}), 400

    # Update password in DB
    alter_client_field(session["client_id"], 'password', new_password)

    return jsonify({"message": "Password updated successfully."})


@app.route("/logout", methods=["POST"])
def logout():
    session.pop("client_id", None)
    return jsonify({"message": "Logged out successfully."})


if __name__ == "__main__":
    app.run(debug=True)
