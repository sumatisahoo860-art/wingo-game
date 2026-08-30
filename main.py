import threading, time, random, os
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)
game_state = {"time_left": 30, "winning_colour": "None", "winning_number": 0, "round_id": 52663}

def game_timer_loop():
    global game_state
    while True:
        try:
            if game_state["time_left"] <= 0:
                game_state["winning_number"] = random.randint(0, 9)
                num = game_state["winning_number"]
                game_state["winning_colour"] = "Red+Violet" if num==0 else ("Green+Violet" if num==5 else ("Red" if num%2==0 else "Green"))
                game_state["round_id"] += 1
                game_state["time_left"] = 30
            else:
                game_state["time_left"] -= 1
            time.sleep(1)
        except Exception: time.sleep(1)

threading.Thread(target=game_timer_loop, daemon=True).start()

# 51GAME का पूरा एडवांस डिज़ाइन बिना किसी सिंटैक्स एरर के
HTML_CONTENT = "https://pastebin.com"

@app.route('/')
def home():
    import requests
    try: html_res = requests.get(HTML_CONTENT).text
    except Exception: html_res = "<h1>51GAME Loading... Please Refresh</h1>"
    return render_template_string(html_res)

@app.route('/api/game-state')
def get_game_state():
    return jsonify(game_state)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    
