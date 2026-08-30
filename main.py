import threading
import time
import random
import os
from flask import Flask, jsonify

app = Flask(__name__)

# गेम स्टेट वैरिएबल्स
game_state = {
    "time_left": 30,
    "winning_colour": "None",
    "round_id": 10001
}

colours = ["Green", "Red", "Violet"]

# रीयल-टाइम बैकग्राउंड टाइमर लूप (Flask के साथ सुरक्षित चलाने के लिए threading का उपयोग)
def game_timer_loop():
    global game_state
    while True:
        try:
            if game_state["time_left"] <= 0:
                game_state["winning_colour"] = random.choice(colours)
                game_state["round_id"] += 1
                game_state["time_left"] = 30
            else:
                game_state["time_left"] -= 1
            time.sleep(1)
        except Exception as e:
            time.sleep(1)

# सर्वर शुरू होते ही बैकग्राउंड में टाइमर थ्रेड चालू करें
timer_thread = threading.Thread(target=game_timer_loop, daemon=True)
timer_thread.start()

@app.route('/')
def home():
    return "<h1>Wingo Flask Server is Running Perfectly!</h1>"

@app.route('/api/game-state', methods=['GET'])
def get_game_state():
    # CORS एरर से बचने के लिए रिस्पॉन्स में हेडर्स जोड़ना
    response = jsonify(game_state)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    # Render द्वारा दिए गए PORT पर सीधे पायथन से रन करना
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
    
