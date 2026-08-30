import threading
import time
import random
import os
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# गेम स्टेट वैरिएबल्स
game_state = {
    "time_left": 30,
    "winning_colour": "None",
    "round_id": 10001
}

colours = ["Green", "Red", "Violet"]

# रीयल-टाइम बैकग्राउंड टाइमर लूप
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

# बैकग्राउंड थ्रेड शुरू करना
timer_thread = threading.Thread(target=game_timer_loop, daemon=True)
timer_thread.start()

# 🎨 गेम का पूरा डिज़ाइन (HTML + CSS + JavaScript)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wingo Colour Trading</title>
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; background-color: #121212; color: #fff; text-align: center; padding: 15px; margin: 0; }
        .app-container { max-width: 500px; margin: 0 auto; background: #1e1e1e; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
        h1 { color: #f1c40f; margin-bottom: 5px; font-size: 26px; }
        .wallet { font-size: 20px; color: #2ecc71; background: #2c2c2c; padding: 10px; border-radius: 8px; margin: 15px 0; font-weight: bold; }
        .timer-box { background: #2c2c2c; padding: 15px; border-radius: 10px; margin-bottom: 20px; }
        .timer-label { font-size: 14px; color: #aaa; text-transform: uppercase; }
        .timer { font-size: 36px; color: #e67e22; font-weight: bold; margin-top: 5px; }
        .btn-container { display: flex; justify-content: space-around; gap: 10px; margin: 20px 0; }
        .btn { flex: 1; padding: 15px 0; font-size: 18px; border: none; cursor: pointer; border-radius: 8px; font-weight: bold; transition: 0.2s; }
        .btn:active { transform: scale(0.95); }
        .btn-green { background-color: #2ecc71; color: white; }
        .btn-violet { background-color: #9b59b6; color: white; }
        .btn-red { background-color: #e74c3c; color: white; }
        .bet-info { background: #2c2c2c; padding: 12px; border-radius: 8px; font-size: 16px; margin: 15px 0; }
        .result-section { margin-top: 25px; border-top: 1px solid #333; padding-top: 15px; }
        .result-box { font-size: 18px; padding: 12px; border-radius: 6px; background-color: #2a2a2a; display: inline-block; min-width: 200px; }
        .win-tag { color: #2ecc71; font-weight: bold; }
        .lose-tag { color: #e74c3c; font-weight: bold; }
    </style>
</head>
<body>
    <div class="app-container">
        <h1>Wingo Colour Trading</h1>
        <p style="color:#888; margin:0;">Game ID: <span id="game-id">------</span></p>
        
        <div class="wallet">💰 Wallet Balance: ₹<span id="balance">1000</span></div>
        
        <div class="timer-box">
            <div class="timer-label">⏱️ Time Remaining</div>
            <div class="timer"><span id="countdown">--</span>s</div>
        </div>

        <h3>Choose a Colour to Bet (₹10):</h3>
        <div class="btn-container">
            <button class="btn btn-green" onclick="selectColour('Green')">Green</button>
            <button class="btn btn-violet" onclick="selectColour('Violet')">Violet</button>
            <button class="btn btn-red" onclick="selectColour('Red')">Red</button>
        </div>

        <div class="bet-info">
            Selected Bet: <strong id="current-bet" style="color: #f1c40f;">None</strong>
        </div>
        
        <div class="result-section">
            <div class="result-box">
                📊 Last Winning Colour: <span id="last-result" style="font-weight: bold; color: #f1c40f;">Waiting...</span>
            </div>
            <p id="game-status" style="font-size: 18px; font-weight: bold; margin-top: 15px;"></p>
        </div>
    </div>

    <script>
        let wallet = 1000;
        let selectedColour = null;
        let lastRoundId = null;

        function selectColour(colour) {
            selectedColour = colour;
            document.getElementById('current-bet').innerText = colour + " (₹10)";
            document.getElementById('game-status').innerText = "Bet Locked! Waiting for result...";
        }

        async function updateGame() {
            try {
                let response = await fetch('/api/game-state');
                let data = await response.json();
                
                document.getElementById('countdown').innerText = data.time_left;
                document.getElementById('game-id').innerText = data.round_id;
                
                if (lastRoundId !== data.round_id) {
                    if (lastRoundId !== null) {
                        document.getElementById('last-result').innerText = data.winning_colour;
                        
                        let statusText = document.getElementById('game-status');
                        if (selectedColour === data.winning_colour) {
                            let winAmount = data.winning_colour === "Violet" ? 45 : 20;
                            wallet += winAmount;
                            statusText.innerHTML = "<span class='win-tag'>🎉 You Won! +₹" + winAmount + "</span>";
                        } else if (selectedColour !== null) {
                            wallet -= 10;
                            statusText.innerHTML = "<span class='lose-tag'>💔 You Lost! -₹10</span>";
                        } else {
                            statusText.innerText = "New round started. Place your bet!";
                        }
                        
                        document.getElementById('balance').innerText = wallet;
                        selectedColour = null;
                        document.getElementById('current-bet').innerText = "None";
                    }
                    lastRoundId = data.round_id;
                }
            } catch (e) {
                console.log("Error syncing game", e);
            }
        }

        setInterval(updateGame, 1000);
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    # अब यह खाली टेक्स्ट की जगह पूरा HTML पेज लोड करेगा
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/game-state', methods=['GET'])
def get_game_state():
    response = jsonify(game_state)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
    
