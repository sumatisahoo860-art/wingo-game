import threading, time, random, os
from flask import Flask, jsonify, render_template

app = Flask(__name__, template_folder='.')

game_state = {
    "time_left": 30,
    "winning_colour": "None",
    "winning_number": 0,
    "winning_size": "None",
    "round_id": 52666,
    "history": [
        {"round": "20260830100052665", "number": 7, "size": "Big", "colour": "Green"},
        {"round": "20260830100052664", "number": 3, "size": "Small", "colour": "Green"},
        {"round": "20260830100052663", "number": 3, "size": "Small", "colour": "Green"}
    ]
}

def game_timer_loop():
    global game_state
    while True:
        try:
            if game_state["time_left"] <= 0:
                num = random.randint(0, 9)
                game_state["winning_number"] = num
                game_state["winning_size"] = "Big" if num >= 5 else "Small"
                col = "Red+Violet" if num == 0 else ("Green+Violet" if num == 5 else ("Red" if num % 2 == 0 else "Green"))
                game_state["winning_colour"] = col
                
                new_hist = {"round": "202608301000" + str(game_state["round_id"]), "number": num, "size": game_state["winning_size"], "colour": col}
                game_state["history"].insert(0, new_hist)
                if len(game_state["history"]) > 6: game_state["history"].pop()
                
                game_state["round_id"] += 1
                game_state["time_left"] = 30
            else:
                game_state["time_left"] -= 1
            time.sleep(1)
        except Exception: time.sleep(1)

threading.Thread(target=game_timer_loop, daemon=True).start()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/game-state')
def get_game_state():
    return jsonify(game_state)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
    
