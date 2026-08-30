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

# बिना किसी बाहरी लिंक के, सीधे ऐप के अंदर 51GAME का असली पीला-सफेद डिजाइन
HTML_CONTENT = """
<!DOCTYPE html><html><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>51GAME Clone</title>
<style>
body{font-family:Arial,sans-serif;background:#f5f5f5;margin:0;padding:0;text-align:center}
.header{background:linear-gradient(135deg,#f1c40f,#f39c12);padding:15px;color:#fff;font-weight:bold;font-size:24px}
.card{background:#fff;margin:15px;padding:20px;border-radius:15px;box-shadow:0 4px 10px rgba(0,0,0,0.05)}
.timer-sec{display:flex;justify-content:space-between;background:#fffced;border:1px dashed #f1c40f;padding:15px;border-radius:10px;margin:15px;align-items:center}
.btn-row{display:flex;justify-content:space-around;margin:15px;gap:10px}
.btn{flex:1;padding:15px 0;border:none;border-radius:8px;font-weight:bold;color:#fff;cursor:pointer;font-size:16px}
.g{background:#00b300}.v{background:#bb33ff}.r{background:#ff3333}
.grid{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin:15px}
.n{width:52px;height:52px;border-radius:50%;border:2px solid #ddd;font-weight:bold;font-size:18px;background:#fff;cursor:pointer;display:flex;align-items:center;justify-content:center;margin:0 auto}
</style></head><body>
<div style='max-width:450px;margin:0 auto;background:#fff;min-height:100vh;padding-bottom:20px'>
<div class='header'>51GAME</div>
<div class='card' style='background:linear-gradient(to bottom, #fff7d6, #fff);border:1px solid #ffe885;'>
<div style='color:#666;font-size:14px'>Wallet balance</div>
<div style='font-size:28px;font-weight:bold;color:#000;margin-top:5px'>₹0.25</div>
</div>
<div class='timer-sec'>
<div style='text-align:left'><h4>WinGo 30sec</h4><p id='rd' style='margin:5px 0 0 0;font-weight:bold'>------</p></div>
<div><div style='font-size:12px;color:#999;margin-bottom:5px'>Time remaining</div>
<div style='font-size:24px;font-weight:bold;background:#000;color:#fff;padding:5px 12px;border-radius:5px;display:inline-block' id='tm'>--s</div>
</div></div>
<div style='margin:15px;font-weight:bold;color:#f39c12'>Selected: <span id='sel' style='color:#000'>None</span></div>
<div class='btn-row'>
<button class='btn g' onclick="document.getElementById('sel').innerText='Green'">Green</button>
<button class='btn v' onclick="document.getElementById('sel').innerText='Violet'">Violet</button>
<button class='btn r' onclick="document.getElementById('sel').innerText='Red'">Red</button>
</div>
<div class='grid'>
<button class='n' style='background:linear-gradient(135deg,#ff3333 50%,#bb33ff 50%);color:#fff' onclick="document.getElementById('sel').innerText='0'">0</button>
<button class='n' style='color:#00b300;border-color:#00b300' onclick="document.getElementById('sel').innerText='1'">1</button>
<button class='n' style='color:#ff3333;border-color:#ff3333' onclick="document.getElementById('sel').innerText='2'">2</button>
<button class='n' style='color:#00b300;border-color:#00b300' onclick="document.getElementById('sel').innerText='3'">3</button>
<button class='n' style='color:#ff3333;border-color:#ff3333' onclick="document.getElementById('sel').innerText='4'">4</button>
<button class='n' style='background:linear-gradient(135deg,#00b300 50%,#bb33ff 50%);color:#fff' onclick="document.getElementById('sel').innerText='5'">5</button>
<button class='n' style='color:#ff3333;border-color:#ff3333' onclick="document.getElementById('sel').innerText='6'">6</button>
<button class='n' style='color:#00b300;border-color:#00b300' onclick="document.getElementById('sel').innerText='7'">7</button>
<button class='n' style='color:#ff3333;border-color:#ff3333' onclick="document.getElementById('sel').innerText='8'">8</button>
<button class='n' style='color:#00b300;border-color:#00b300' onclick="document.getElementById('sel').innerText='9'">9</button>
</div></div>
<script>
async function sync(){
try{
let res=await fetch('/api/game-state');let d=await res.json();
document.getElementById('tm').innerText=d.time_left+'s';
document.getElementById('rd').innerText='202608291000'+d.round_id;
}catch(e){}
}setInterval(sync,1000);
</script></body></html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_CONTENT)

@app.route('/api/game-state')
def get_game_state():
    return jsonify(game_state)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
