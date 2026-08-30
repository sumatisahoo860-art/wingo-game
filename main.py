import threading, time, random, os
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# शुरुआती वॉलेट बैलेंस ₹1,00,000 और गेम स्टेट सेटिंग्स
game_state = {
    "time_left": 30,
    "winning_colour": "None",
    "winning_number": 0,
    "winning_size": "None",
    "round_id": 52664,
    "history": [
        {"round": "20260830100052663", "number": 3, "size": "Small", "colour": "Green"},
        {"round": "20260830100052662", "number": 8, "size": "Big", "colour": "Red"},
        {"round": "20260830100052661", "number": 0, "size": "Small", "colour": "Red+Violet"}
    ]
}

def game_timer_loop():
    global game_state
    while True:
        try:
            if game_state["time_left"] <= 0:
                # 0-9 रैंडम नंबर और साइज (Big/Small) तय करना
                num = random.randint(0, 9)
                game_state["winning_number"] = num
                game_state["winning_size"] = "Big" if num >= 5 else "Small"
                
                # प्रोफेशनल कलर कोडिंग नियम
                if num == 0:
                    col = "Red+Violet"
                elif num == 5:
                    col = "Green+Violet"
                elif num % 2 == 0:
                    col = "Red"
                else:
                    col = "Green"
                game_state["winning_colour"] = col
                
                # हिस्ट्री टेबल में नया डेटा सबसे ऊपर जोड़ना
                new_hist = {
                    "round": "202608301000" + str(game_state["round_id"]),
                    "number": num,
                    "size": game_state["winning_size"],
                    "colour": col
                }
                game_state["history"].insert(0, new_hist)
                if len(game_state["history"]) > 6: 
                    game_state["history"].pop()
                
                game_state["round_id"] += 1
                game_state["time_left"] = 30
            else:
                game_state["time_left"] -= 1
            time.sleep(1)
        except Exception: 
            time.sleep(1)

threading.Thread(target=game_timer_loop, daemon=True).start()

# 51GAME का एडवांस UI लेआउट (Big/Small, Multipliers, Live History Table)
HTML_CONTENT = """
<!DOCTYPE html><html><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>51GAME Professional</title>
<style>
body{font-family:Arial,sans-serif;background:#f5f5f5;margin:0;padding:0;text-align:center}
.header{background:linear-gradient(135deg,#f1c40f,#f39c12);padding:15px;color:#fff;font-weight:bold;font-size:24px}
.card{background:#fff;margin:15px;padding:15px;border-radius:12px;box-shadow:0 4px 10px rgba(0,0,0,0.05)}
.timer-sec{display:flex;justify-content:space-between;background:#fffced;border:1px dashed #f1c40f;padding:15px;border-radius:10px;margin:15px;align-items:center}
.btn-row{display:flex;justify-content:space-around;margin:15px;gap:8px}
.btn{flex:1;padding:12px 0;border:none;border-radius:8px;font-weight:bold;color:#fff;cursor:pointer;font-size:15px}
.g{background:#00b300}.v{background:#bb33ff}.r{background:#ff3333}
.b-btn{background:#e67e22}.s-btn{background:#3498db}
.grid{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin:15px}
.n{width:48px;height:48px;border-radius:50%;border:2px solid #ddd;font-weight:bold;font-size:16px;background:#fff;cursor:pointer;display:flex;align-items:center;justify-content:center;margin:0 auto}
.m-row{display:flex;justify-content:space-between;margin:15px;background:#fafafa;padding:6px;border-radius:20px;gap:4px;border:1px solid #eee}
.m-btn{padding:5px 10px;border:1px solid #ddd;background:#fff;border-radius:15px;font-size:11px;font-weight:bold;cursor:pointer}
.m-act{background:#00b300;color:#fff;border-color:#00b300}
.hist-table{width:100%;border-collapse:collapse;margin-top:10px;font-size:13px;text-align:center}
.hist-table th{background:#eee;padding:8px;color:#555}
.hist-table td{padding:8px;border-bottom:1px solid #eee}
.dot{display:inline-block;width:12px;height:12px;border-radius:50%;vertical-align:middle}
</style></head><body>
<div style='max-width:450px;margin:0 auto;background:#fff;min-height:100vh;padding-bottom:30px;box-shadow:0 0 10px rgba(0,0,0,0.1)'>
<div class='header'>51GAME</div>
<div class='card' style='background:linear-gradient(to bottom, #fff7d6, #fff);border:1px solid #ffe885;'>
<div style='color:#666;font-size:13px'>Wallet balance</div>
<div style='font-size:28px;font-weight:bold;color:#000;margin-top:5px'>₹<span id='bal'>100000.00</span></div>
</div>
<div class='timer-sec'>
<div style='text-align:left'><h4>WinGo 30sec</h4><p id='rd' style='margin:5px 0 0 0;font-weight:bold;color:#333'>------</p></div>
<div><div style='font-size:12px;color:#999;margin-bottom:5px'>Time remaining</div>
<div style='font-size:22px;font-weight:bold;background:#000;color:#fff;padding:5px 12px;border-radius:5px;display:inline-block' id='tm'>--s</div>
</div></div>
<div style='margin:15px;font-weight:bold;color:#e67e22;background:#fffcf0;padding:8px;border-radius:6px;border:1px solid #ffeaa7'>
Selected: <span id='sel' style='color:#000'>None</span> <span id='mtxt' style='color:#00b300'></span>
</div>
<div class='btn-row'>
<button class='btn g' onclick="bet('Green')">Green</button>
<button class='btn v' onclick="bet('Violet')">Violet</button>
<button class='btn r' onclick="bet('Red')">Red</button>
</div>
<div class='btn-row' style='margin-top:-5px'>
<button class='btn b-btn' onclick="bet('Big')">Big</button>
<button class='btn s-btn' onclick="bet('Small')">Small</button>
</div>
<div class='grid'>
<button class='n' style='background:linear-gradient(135deg,#ff3333 50%,#bb33ff 50%);color:#fff' onclick="bet('0')">0</button>
<button class='n' style='color:#00b300;border-color:#00b300' onclick="bet('1')">1</button>
<button class='n' style='color:#ff3333;border-color:#ff3333' onclick="bet('2')">2</button>
<button class='n' style='color:#00b300;border-color:#00b300' onclick="bet('3')">3</button>
<button class='n' style='color:#ff3333;border-color:#ff3333' onclick="bet('4')">4</button>
<button class='n' style='background:linear-gradient(135deg,#00b300 50%,#bb33ff 50%);color:#fff' onclick="bet('5')">5</button>
<button class='n' style='color:#ff3333;border-color:#ff3333' onclick="bet('6')">6</button>
<button class='n' style='color:#00b300;border-color:#00b300' onclick="bet('7')">7</button>
<button class='n' style='color:#ff3333;border-color:#ff3333' onclick="bet('8')">8</button>
<button class='n' style='color:#00b300;border-color:#00b300' onclick="bet('9')">9</button>
</div>
<div class='m-row'>
<button class='m-btn m-act' onclick='setM(1,this)'>X1</button>
<button class='m-btn' onclick='setM(5,this)'>X5</button>
<button class='m-btn' onclick='setM(10,this)'>X10</button>
<button class='m-btn' onclick='setM(20,this)'>X20</button>
<button class='m-btn' onclick='setM(50,this)'>X50</button>
<button class='m-btn' onclick='setM(100,this)'>X100</button>
</div>
<div class='card' style='text-align:left'>
<h3 style='margin:0 0 10px 0;font-size:16px;color:#333;border-bottom:2px solid #f1c40f;padding-bottom:5px'>📊 Game History (WinGo 30s)</h3>
<table class='hist-table'><thead><tr><th>Period</th><th>Number</th><th>Size</th><th>Colour</th></tr></thead><tbody id='hist'></tbody></table>
</div></div>
<script>
let u_wallet = 100000;
let u_sel = null;
let u_mult = 1;
let base_bet = 10;
let last_id = null;

function bet(val) {
    u_sel = val;
    document.getElementById('sel').innerText = val;
    document.getElementById('mtxt').innerText = " (₹" + (base_bet * u_mult) + ")";
}

function setM(val, el) {
    u_mult = val;
    document.querySelectorAll('.m-btn').forEach(b => b.classList.remove('m-act'));
    el.classList.add('m-act');
    if(u_sel) bet(u_sel);
}

async function sync(){
try{
    let res = await fetch('/api/game-state');
    let d = await res.json();
    document.getElementById('tm').innerText = d.time_left + 's';
    let current_round = '202608301000' + d.round_id;
    document.getElementById('rd').innerText = current_round;
    
    let h_html = "";
    d.history.forEach(h => {
        let c_color = '#00b300';
        if (h.colour.includes('Red')) c_color = '#ff3333';
        if (h.colour == 'Red+Violet') c_color = 'linear-gradient(135deg,#ff3333 50%,#bb33ff 50%)';
        if (h.colour == 'Green+Violet') c_color = 'linear-gradient(135deg,#00b300 50%,#bb33ff 50%)';
        
        let display_dot = c_color.includes('gradient') ? `<span class='dot' style='background:${c_color}'></span>` : `<span class='dot' style='background:${c_color}'></span>`;
        
        h_html += `<tr><td>${h.round}</td><td style='font-weight:bold;'>${h.number}</td><td>${h.size}</td><td>${display_dot}</td></tr>`;
    });
    document.getElementById('hist').innerHTML = h_html;

    if (last_id !== d.round_id) {
        if (last_id !== null && u_sel !== null) {
            let total_bet = base_bet * u_mult;
            let win = false;
            let win_amt = 0;
            
            if (u_sel === d.winning_number.toString()) { win = true; win_amt = total_bet * 9; }
            else if (u_sel === d.winning_size) { win = true; win_amt = total_bet * 2; }
            else if (d.winning_colour.includes(u_sel)) {
                win = true;
                win_amt = u_sel === 'Violet' ? total_bet * 4.5 : total_bet * 2;
            }
            
            if (win) {
                u_wallet += (win_amt - total_bet);
                alert(`🎉 WIN! Result: ${d.winning_number} (${d.winning_size}). You Won ₹${win_amt}`);
            } else {
                u_wallet -= total_bet;
                alert(`💔 LOST! Result: ${d.winning_number} (${d.winning_size}). Lost ₹${total_bet}`);
            }
            document.getElementById('bal').innerText = u_wallet.toFixed(2);
            u_sel = null;
            document.getElementById('sel').innerText = 'None';
            document.getElementById('mtxt').innerText = '';
        }
        last_id = d.round_id;
                }
