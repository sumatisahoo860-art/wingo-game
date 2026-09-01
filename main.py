import time
import random
from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

# Game memory storage configuration (Safe Automatic Version)
game_data = {
    "start_period": 20260901001,
    "start_time": time.time(),
    "history": [],
    "user_wallets": {"user123": 45000}, # Aapka 45k virtual balance locked hai
    "user_bets": {} 
}

def update_and_get_state():
    current_time = time.time()
    elapsed_time = current_time - game_data["start_time"]
    
    rounds_passed = int(elapsed_time // 30)
    current_timer = 30 - int(elapsed_time % 30)
    current_period = game_data["start_period"] + rounds_passed
    
    last_calculated_period = game_data["start_period"] + len(game_data["history"])
    
    while last_calculated_period < current_period:
        # 100% Pure Automatic Random Selection
        win_color = random.choice(['red', 'green', 'violet'])
        game_data["history"].append({"period": last_calculated_period, "result": win_color})
        
        if last_calculated_period in game_data["user_bets"]:
            for user_id, bets_list in game_data["user_bets"][last_calculated_period].items():
                total_winnings = 0
                for bet_info in bets_list:
                    if bet_info["color"] == win_color:
                        multiplier = 4.5 if win_color == 'violet' else 2.0
                        total_winnings += int(bet_info["amount"] * multiplier)
                game_data["user_wallets"][user_id] += total_winnings
        last_calculated_period += 1
    return current_period, current_timer

HTML_UI = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wingo Color Trading Game</title>
    <style>
        body { font-family: 'Arial', sans-serif; background: #f5f5f5; text-align: center; padding: 10px; margin: 0; }
        .app-container { max-width: 450px; background: white; margin: 0 auto; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); padding: 15px; min-height: 90vh; position: relative; }
        .header { background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 15px; border-radius: 10px; font-weight: bold; }
        .balance-box { font-size: 24px; font-weight: bold; margin: 15px 0; color: #333; }
        .game-info { display: flex; justify-content: space-between; background: #fdf2e9; padding: 10px; border-radius: 8px; margin: 15px 0; border: 1px solid #ffeb3b; }
        .timer { font-size: 20px; font-weight: bold; color: #ff5722; }
        .bet-buttons { display: flex; justify-content: space-around; margin: 20px 0; }
        .btn { padding: 12px 25px; font-size: 16px; border: none; border-radius: 25px; color: white; font-weight: bold; cursor: pointer; width: 28%; }
        .green { background: #4caf50; } .violet { background: #9c27b0; } .red { background: #f44336; }
        .input-box { width: 80%; padding: 10px; font-size: 16px; border-radius: 8px; border: 1px solid #ccc; text-align: center; margin-bottom: 10px; }
        .history { text-align: left; background: #fafafa; padding: 10px; border-radius: 8px; margin-top: 20px; border: 1px solid #eee; }
        .history-item { display: flex; justify-content: space-between; padding: 8px; border-bottom: 1px solid #eee; }
        .badge { padding: 3px 8px; border-radius: 4px; color: white; font-weight: bold; text-transform: uppercase; }
        
        /* Premium Win Picture Popup Overlay */
        .popup-overlay { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.6); z-index: 1000; justify-content: center; align-items: center; }
        .popup-card { background: white; padding: 20px; border-radius: 15px; max-width: 320px; width: 80%; text-align: center; box-shadow: 0 5px 20px rgba(0,0,0,0.3); animation: pop 0.3s ease-out; }
        @keyframes pop { from { transform: scale(0.7); opacity: 0; } to { transform: scale(1); opacity: 1; } }
        .win-img { width: 120px; height: 120px; margin-bottom: 15px; }
        .close-popup { background: #ff5722; color: white; border: none; padding: 10px 20px; border-radius: 20px; font-weight: bold; cursor: pointer; margin-top: 15px; width: 100%; }
    </style>
</head>
<body>

    <!-- 🏆 WINNING CELEBRATION POPUP DIALOG -->
    <div class="popup-overlay" id="win-popup">
        <div class="popup-card">
            <svg class="win-img" viewBox="0 0 24 24" fill="none" xmlns="http://w3.org"><circle cx="12" cy="12" r="10" fill="#FFD700"/><path d="M12 6V14M12 14L9 11M12 14L15 11" stroke="#FFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M8 18H16" stroke="#FFF" stroke-width="2" stroke-linecap="round"/></svg>
            <h2 style="color: #4caf50; margin: 5px 0;">🎉 YOU WIN!</h2>
            <p style="font-size: 16px; color: #555; margin: 10px 0;">Congratulations! Your prediction was 100% correct.</p>
            <button class="close-popup" onclick="closePopup()">Awesome!</button>
        </div>
    </div>

    <div class="app-container">
        <div class="header">🎮 WINGO COLOR TRADING</div>
        <div class="balance-box">🪙 Wallet: <span id="balance">45000</span> Coins</div>
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
        let lastLoggedPeriod = null;
        let lastWalletBalance = 45000;

        function updateStatus() {
            fetch('/api/game-status')
                .then(res => res.json())
                .then(data => {
                    document.getElementById('period-id').innerText = data.period;
                    document.getElementById('time-left').innerText = data.timer;
                    document.getElementById('balance').innerText = data.wallet;
                    
                    if(lastLoggedPeriod && data.period !== lastLoggedPeriod && data.history.length > 0) {
                        let lastResult = data.history[data.history.length - 1];
                        
                        if (data.wallet > lastWalletBalance) {
                            document.getElementById('win-popup').style.display = 'flex';
                        } else {
                            alert(`Round ${lastResult.period} Ended! Winner color is: ${lastResult.result.toUpperCase()}`);
                        }
                    }
                    lastLoggedPeriod = data.period;
                    lastWalletBalance = data.wallet;
                    
                    let historyHtml = '';
                    let displayHistory = [...data.history].reverse().slice(0, 7);
                    displayHistory.forEach(item => {
                        let colorClass = item.result === 'green' ? 'green' : (item.result === 'red' ? 'red' : 'violet');
                        historyHtml += `<div class="history-item"><span>ID: ${item.period}</span> <span class="badge ${colorClass}">${item.result}</span></div>`;
                    });
                    document.getElementById('history-logs').innerHTML = historyHtml || 'No data';
                });
        }
        function placeBet(color) {
            let amount = parseInt(document.getElementById('bet-amount').value);
            fetch('/api/place-bet', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ color: color, amount: amount, user_id: 'user123' })
            }).then(res => res.json()).then(data => {
                if(data.success) {
                    document.getElementById('balance').innerText = data.new_balance;
                    lastWalletBalance = data.new_balance;
                    alert(`Bet added: ${color.toUpperCase()} pe ${amount} Coins lag gye!`);
                } else { alert(data.message); }
            });
        }
        function closePopup() {
            document.getElementById('win-popup').style.display = 'none';
        }
        setInterval(updateStatus, 1000);
        updateStatus();
    </script>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(HTML_UI)

@app.route('/api/game-status', methods=['GET'])
def get_status():
    current_period, current_timer = update_and_get_state()
    return jsonify({"period": current_period, "timer": current_timer, "history": game_data["history"], "wallet": game_data["user_wallets"]["user123"]})

@app.route('/api/place-bet', methods=['POST'])
def place_bet():
    data = request.json
    color, amount, user_id = data.get('color'), int(data.get('amount', 0)), data.get('user_id', 'user123')
    current_period, current_timer = update_and_get_state()
    if current_timer <= 5: return jsonify({"success": False, "message": "Time khatam!"})
    if game_data["user_wallets"][user_id] < amount: return jsonify({"success": False, "message": "Balance kam hai!"})
    game_data["user_wallets"][user_id] -= amount
    if current_period not in game_data["user_bets"]: game_data["user_bets"][current_period] = {}
    if user_id not in game_data["user_bets"][current_period]: game_data["user_bets"][current_period][user_id] = []
    game_data["user_bets"][current_period][user_id].append({"color": color, "amount": amount})
    
