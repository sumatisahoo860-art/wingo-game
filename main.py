import time
import random
from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

# Game data ko memory me save rakhne ke liye variables
game_data = {
    "period": 20260901001,
    "timer": 30,
    "current_bets": [],
    "history": [],
    "admin_choice": None  # Isse aap result control kar sakte hain
}

# HTML aur UI Code (Single file deployment ke liye)
HTML_UI = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wingo Color Trading Game</title>
    <style>
        body { font-family: 'Arial', sans-serif; background: #f5f5f5; text-align: center; padding: 10px; margin: 0; }
        .app-container { max-width: 450px; background: white; margin: 0 auto; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); padding: 15px; min-height: 90vh; }
        .header { background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 15px; border-radius: 10px; font-weight: bold; }
        .balance-box { font-size: 24px; font-weight: bold; margin: 15px 0; color: #333; }
        .game-info { display: flex; justify-content: space-between; background: #fdf2e9; padding: 10px; border-radius: 8px; margin: 15px 0; border: 1px solid #ffeb3b; }
        .timer { font-size: 20px; font-weight: bold; color: #ff5722; }
        .bet-buttons { display: flex; justify-content: space-around; margin: 20px 0; }
        .btn { padding: 12px 25px; font-size: 16px; border: none; border-radius: 25px; color: white; font-weight: bold; cursor: pointer; transition: 0.2s; width: 28%; }
        .green { background: #4caf50; box-shadow: 0 4px #2e7d32; }
        .violet { background: #9c27b0; box-shadow: 0 4px #6a1b9a; }
        .red { background: #f44336; box-shadow: 0 4px #c62828; }
        .btn:active { transform: translateY(4px); box-shadow: none; }
        .input-box { width: 80%; padding: 10px; font-size: 16px; border-radius: 8px; border: 1px solid #ccc; text-align: center; margin-bottom: 10px; }
        .history { text-align: left; background: #fafafa; padding: 10px; border-radius: 8px; margin-top: 20px; border: 1px solid #eee; }
        .history-item { display: flex; justify-content: space-between; padding: 8px; border-bottom: 1px solid #eee; }
        .badge { padding: 3px 8px; border-radius: 4px; color: white; font-weight: bold; text-transform: uppercase; }
    </style>
</head>
<body>
    <div class="app-container">
        <div class="header">🎮 WINGO COLOR TRADING</div>
        
        <div class="balance-box">🪙 Wallet: <span id="balance">10000</span> Coins</div>
        
        <div class="game-info">
            <div>Period: <br><strong id="period-id">-</strong></div>
            <div class="timer">Time Left: <br><span id="time-left">30</span>s</div>
        </div>

        <h3>Enter Amount to Bet:</h3>
        <input type="number" id="bet-amount" class="input-box" value="100" min="10">
        
        <div class="bet-buttons">
            <button class="btn green" onclick="placeBet('green')">Green</button>
            <button class="btn violet" onclick="placeBet('violet')">Violet</button>
            <button class="btn red" onclick="placeBet('red')">Red</button>
        </div>

        <div class="history">
            <h4>📜 Last Game Results</h4>
            <div id="history-logs">Loading...</div>
        </div>
    </div>

    <script>
        let walletBalance = 10000;

        function updateStatus() {
            fetch('/api/game-status')
                .then(res => res.json())
                .then(data => {
                    document.getElementById('period-id').innerText = data.period;
                    document.getElementById('time-left').innerText = data.timer;
                    
                    let historyHtml = '';
                    data.history.reverse().forEach(item => {
                        let colorClass = item.result === 'green' ? 'green' : (item.result === 'red' ? 'red' : 'violet');
                        historyHtml += `<div class="history-item"><span>ID: ${item.period}</span> <span class="badge ${colorClass}">${item.result}</span></div>`;
                    });
                    document.getElementById('history-logs').innerHTML = historyHtml || 'No data';
                });
        }

        function placeBet(color) {
            let amount = parseInt(document.getElementById('bet-amount').value);
            if(amount > walletBalance) { alert("Balance kam hai!"); return; }
            
            fetch('/api/place-bet', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ color: color, amount: amount })
            })
            .then(res => res.json())
            .then(data => {
                if(data.success) {
                    walletBalance -= amount;
                    document.getElementById('balance').innerText = walletBalance;
                    alert("Bet successful on " + color.toUpperCase());
                }
            });
        }

        // Har ek second me UI update hoga
        setInterval(updateStatus, 1000);
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_UI)

# Live status API data fetch karne ke liye
@app.route('/api/game-status', methods=['GET'])
def get_status():
    return jsonify(game_data)

# Bet lagane ki API
@app.route('/api/place-bet', methods=['POST'])
def place_bet():
    data = request.json
    game_data['current_bets'].append(data)
    return jsonify({"success": True})

# Admin Control Panel URL: Yahan se aap result badal sakte hain
# Example URL: ://onrender.com
@app.route('/admin/control', methods=['GET'])
def admin_control():
    color = request.args.get('color')
    if color in ['red', 'green', 'violet']:
        game_data['admin_choice'] = color
        return f"Success! Next winning color forced to: {color.upper()}"
    return "Invalid color! Use red, green, or violet."

# Background calculation simulator jo live cloud server par timer chalayega
def run_timer_loop():
    while True:
        time.sleep(1)
        if game_data['timer'] > 0:
            game_data['timer'] -= 1
        else:
            # Jab timer 0 hoga toh result announce hoga
            if game_data['admin_choice']:
                win_color = game_data['admin_choice']
                game_data['admin_choice'] = None # Override reset
            else:
                win_color = random.choice(['red', 'green', 'violet'])
                
            game_data['history'].append({"period": game_data['period'], "result": win_color})
            game_data['period'] += 1
            game_data['timer'] = 30 # Timer resets to 30s
            game_data['current_bets'] = []

# Background thread starter
import threading
threading.Thread(target=run_timer_loop, daemon=True).start()

if __name__ == '__main__':
    # Render port mapping configuration
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
