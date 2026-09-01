import time
import random
from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

# Game memory storage configuration
game_data = {
    "start_period": 20260901001,
    "start_time": time.time(),
    "history": [],
    "admin_choice": None,         
    "user_wallets": {"user123": 10000}, 
    "user_bets": {}               
}

# Clear logic for matching colors and numbers
def get_color_for_number(num):
    if num == 0 or num == 5:
        return 'violet'
    elif num % 2 == 0:
        return 'red'
    else:
        return 'green'

def update_and_get_state():
    current_time = time.time()
    elapsed_time = current_time - game_data["start_time"]
    
    rounds_passed = int(elapsed_time // 30)
    current_timer = 30 - int(elapsed_time % 30)
    current_period = game_data["start_period"] + rounds_passed
    
    last_calculated_period = game_data["start_period"] + len(game_data["history"])
    
    while last_calculated_period < current_period:
        if game_data["admin_choice"]:
            choice = game_data["admin_choice"]
            game_data["admin_choice"] = None 
            if choice.isdigit():
                win_number = int(choice)
                win_color = get_color_for_number(win_number)
            else:
                win_color = choice
                if win_color == 'violet':
                    win_number = 0
                elif win_color == 'red':
                    win_number = 2
                else:
                    win_number = 1
        else:
            win_number = random.randint(0, 9)
            win_color = get_color_for_number(win_number)
        
        game_data["history"].append({
            "period": last_calculated_period, 
            "result_color": win_color, 
            "result_number": win_number
        })
        
        if last_calculated_period in game_data["user_bets"]:
            for user_id, bets_list in game_data["user_bets"][last_calculated_period].items():
                total_winnings = 0
                for bet_info in bets_list:
                    if bet_info["type"] == "color" and bet_info["choice"] == win_color:
                        multiplier = 4.5 if win_color == 'violet' else 2.0
                        total_winnings += int(bet_info["amount"] * multiplier)
                    elif bet_info["type"] == "number" and int(bet_info["choice"]) == win_number:
                        total_winnings += int(bet_info["amount"] * 9.0)
                
                game_data["user_wallets"][user_id] += total_winnings
        
        last_calculated_period += 1
        
    return current_period, current_timer

HTML_UI = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wingo Color & Number Trading Game</title>
    <style>
        body { font-family: 'Arial', sans-serif; background: #f5f5f5; text-align: center; padding: 10px; margin: 0; }
        .app-container { max-width: 450px; background: white; margin: 0 auto; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); padding: 15px; min-height: 90vh; }
        .header { background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 15px; border-radius: 10px; font-weight: bold; }
        .balance-box { font-size: 24px; font-weight: bold; margin: 15px 0; color: #333; }
        .game-info { display: flex; justify-content: space-between; background: #fdf2e9; padding: 10px; border-radius: 8px; margin: 15px 0; border: 1px solid #ffeb3b; }
        .timer { font-size: 20px; font-weight: bold; color: #ff5722; }
        
        .bet-buttons { display: flex; justify-content: space-around; margin: 15px 0; }
        .btn { padding: 12px 25px; font-size: 16px; border: none; border-radius: 25px; color: white; font-weight: bold; cursor: pointer; transition: 0.2s; width: 28%; }
        .green { background: #4caf50; box-shadow: 0 4px #2e7d32; }
        .violet { background: #9c27b0; box-shadow: 0 4px #6a1b9a; }
        .red { background: #f44336; box-shadow: 0 4px #c62828; }
        
        .number-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; margin: 15px 0; }
        .num-btn { padding: 12px; font-size: 16px; font-weight: bold; border: none; border-radius: 8px; color: white; cursor: pointer; }
        .n0, .n5 { background: #9c27b0; } 
        .n1, .n3, .n7, .n9 { background: #4caf50; } 
        .n2, .n4, .n6, .n8 { background: #f44336; } 
        
        .btn:active, .num-btn:active { transform: translateY(2px); box-shadow: none; }
        .input-box { width: 80%; padding: 10px; font-size: 16px; border-radius: 8px; border: 1px solid #ccc; text-align: center; margin-bottom: 10px; }
        .history { text-align: left; background: #fafafa; padding: 10px; border-radius: 8px; margin-top: 20px; border: 1px solid #eee; }
        .history-item { display: flex; justify-content: space-between; padding: 8px; border-bottom: 1px solid #eee; align-items: center; }
        .badge { padding: 4px 10px; border-radius: 4px; color: white; font-weight: bold; text-transform: uppercase; font-size: 12px; }
        .num-circle { display: inline-block; width: 24px; height: 24px; border-radius: 50%; background: #333; color: white; text-align: center; line-height: 24px; font-weight: bold; margin-left: 5px; }
    </style>
</head>
<body>
    <div class="app-container">
        <div class="header">🎮 WINGO COLOR & NUMBER</div>
        
        <div class="balance-box">🪙 Wallet: <span id="balance">10000</span> Coins</div>
        
        <div class="game-info">
            <div>Period: <br><strong id="period-id">-</strong></div>
            <div class="timer">Time Left: <br><span id="time-left">30</span>s</div>
        </div>

        <h3>Enter Amount to Bet:</h3>
        <input type="number" id="bet-amount" class="input-box" value="100" min="10">
        
        <div class="bet-buttons">
            <button class="btn green" onclick="placeBet('color', 'green')">Green</button>
            <button class="btn violet" onclick="placeBet('color', 'violet')">Violet</button>
            <button class="btn red" onclick="placeBet('color', 'red')">Red</button>
        </div>

        <h3>Select Number (9x Profit):</h3>
        <div class="number-grid">
            <button class="num-btn n0" onclick="placeBet('number', '0')">0</button>
            <button class="num-btn n1" onclick="placeBet('number', '1')">1</button>
            <button class="num-btn n2" onclick="placeBet('number', '2')">2</button>
            <button class="num-btn n3" onclick="placeBet('number', '3')">3</button>
            <button class="num-btn n4" onclick="placeBet('number', '4')">4</button>
            <button class="num-btn n5" onclick="placeBet('number', '5')">5</button>
            <button class="num-btn n6" onclick="placeBet('number', '6')">6</button>
            <button class="num-btn n7" onclick="placeBet('number', '7')">7</button>
            <button class="num-btn n8" onclick="placeBet('number', '8')">8</button>
            <button class="num-btn n9" onclick="placeBet('number', '9')">9</button>
        </div>

        <div class="history">
            <h4>📜 Last Game Results</h4>
            <div id="history-logs">Loading...</div>
        </div>
    </div>

    <script>
        let lastLoggedPeriod = null;

        function updateStatus() {
            fetch('/api/game-status')
                .then(res => res.json())
                .then(data => {
                    document.getElementById('period-id').innerText = data.period;
                    document.getElementById('time-left').innerText = data.timer;
                    document.getElementById('balance').innerText = data.wallet;
                    
                    if(lastLoggedPeriod && data.period !== lastLoggedPeriod && data.history.length > 0) {
                        let lastResult = data.history[data.history.length - 1];
                        alert(`Round ${lastResult.period} Ended! Winner: ${lastResult.result_color.toUpperCase()} (Number ${lastResult.result_number})`);
                    }
                    lastLoggedPeriod = data.period;
                    
                    let historyHtml = '';
                    let displayHistory = [...data.history].reverse().slice(0, 7);
                    displayHistory.forEach(item => {
                        let colorClass = item.result_color === 'green' ? 'green' : (item.result_color === 'red' ? 'red' : 'violet');
                        historyHtml += `
                            <div class="history-item">
                                <span>ID: ${item.period}</span> 
                                <div>
                                    <span class="badge ${colorClass}">${item.result_color}</span>
                                    <span class="num-circle">${item.result_number}</span>
                                </div>
                            </div>`;
                    });
                    document.getElementById('history-logs').innerHTML = historyHtml || 'No data';
                });
        }

        function placeBet(type, choice) {
            let amount = parseInt(document.getElementById('bet-amount').value);
            let currentBalance = parseInt(document.getElementById('balance').innerText);
            if(amount > currentBalance) { alert("Wallet me balance kam hai!"); return; }
            
            fetch('/api/place-bet', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ type: type, choice: choice, amount: amount, user_id: 'user123' })
            })
            .then(res => res.json())
            .then(data => {
                if(data.success) {
                    document.getElementById('balance').innerText = data.new_balance;
                    alert(`Bet added: ${choice.toUpperCase()} pe ${amount} Coins lag gye!`);
                    
