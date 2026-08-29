import random, os
from flask import Flask, render_template_string, request, jsonify
app = Flask(__name__)
db = {"bal": 1000.0, "msg": "राशि डालें और रंग चुनें!", "hist": ["Red", "Green"], "color": None, "bet_amt": 0.0, "pid": 101}

html = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>51Game</title>
<style>
    body { background:#1a1a24; color:#fff; font-family:sans-serif; text-align:center; padding:15px; }
    .box { width:100%; max-width:400px; background:#222232; border-radius:15px; padding:20px; margin:auto; }
    input { width:100%; padding:10px; background:rgba(255,255,255,0.1); border:none; border-radius:8px; color:#fff; margin-bottom:15px; text-align:center; }
    button { width:100%; padding:12px; background:linear-gradient(90deg, #ff416c, #ff4b2b); border:none; border-radius:8px; color:#fff; font-weight:bold; cursor:pointer; }
    .card { background:linear-gradient(135deg, #2b5876, #4e4376); border-radius:12px; padding:15px; margin:15px 0; }
    .cb { padding:10px; border:none; border-radius:8px; font-weight:bold; color:#fff; margin:4px; width:28%; }
    .bg { background:#00b0ff; } .bv { background:#9c27b0; } .br { background:#ff3b30; }
    .dot { display:inline-block; width:40px; padding:5px; margin:3px; border-radius:5px; font-weight:bold; background:#555; }
</style></head><body>
<div id="p-login" class="box">
    <h2>👑 51Game Login</h2><br>
    <input type="text" id="u" placeholder="Username (admin)">
    <input type="password" id="p" placeholder="Password (1245)">
    <button onclick="if(u.value=='admin'&&p.value=='1245'){pLogin.style.display='none';pDash.style.display='block';}else{alert('Wrong!');}">LOGIN</button>
</div>
<div id="p-dash" class="box" style="display:none;">
    <h2>Dashboard ✨</h2>
    <div class="card"><h3>BALANCE</h3><h2 style="color:#ffdf00;">₹ <span class="b-val">1000</span></h2></div>
    <button onclick="pDash.style.display='none';pGame.style.display='block';">🎯 Play Win Go Now</button>
</div>
<div id="p-game" class="box" style="display:none;">
    <div style="display:flex; justify-content:space-between;"><button onclick="pGame.style.display='none';pDash.style.display='block';" style="width:auto; padding:5px 10px;">⬅ Back</button><span>Win Go 1Min</span></div>
    <div class="card"><h3>BALANCE</h3><h2>₹ <span class="b-val">1000</span></h2></div>
    <h2 id="count" style="color:#00ffcc;">00:30</h2>
    <input type="number" id="amt" value="100"><br>
    <button onclick="bet('Green')" class="cb bg">Green</button><button onclick="bet('Violet')" class="cb bv">Violet</button><button onclick="bet('Red')" class="cb br">Red</button>
    <div style="margin:15px 0; background:#1a1a24; padding:10px; border-radius:8px;" id="st">Prediction Open!</div>
    <div id="hist"></div>
</div>
<script>
    let time = 30, pLogin=document.getElementById('p-login'), pDash=document.getElementById('p-dash'), pGame=document.getElementById('p-game'), u=document.getElementById('u'), p=document.getElementById('p');
    function bet(c) {
        if(time<=5) return;
        fetch('/api', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({a:'bet', c:c, amt:document.getElementById('amt').value})})
        .then(r=>r.json()).then(d=>{ if(d.status=='ok'){ update(d); st.innerText="Bet locked on "+c; } else { alert(d.msg); } });
    }
    function update(d) { document.querySelectorAll('.b-val').forEach(e=>e.innerText=d.bal.toFixed(2)); }
    setInterval(() => {
        time--; if(time<0) time=30;
        count.innerText = `00:${time<10?'0'+time:time}`;
        if(time<=5) st.innerText = "🛑 Locked!";
        if(time===0) {
            fetch('/api', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({a:'res'})})
            .then(r=>r.json()).then(d=>{ update(d); st.innerText=d.msg; });
        }
    }, 1000);
</script>
</body></html>
"""

@app.route('/')
def home(): return render_template_string(html, db=db)

@app.route('/api', methods=['POST'])
def api():
    req = request.json; act = req.get('a')
    if act == 'bet':
        amt = float(req.get('amt'))
        if db["bal"] >= amt:
            db["bal"] -= amt; db["color"] = req.get('c'); db["bet_amt"] = amt
            return jsonify({"status": "ok", "bal": db["bal"]})
        return jsonify({"status": "err", "msg": "Low Balance!"})
    if act == 'res':
        win = random.choice(["Green", "Red", "Violet", "Green", "Red"])
        if db["color"]:
            m = 3.0 if win == "Violet" else 2.0
            if db["color"] == win:
                pz = db["bet_amt"] * m; db["bal"] += pz
                db["msg"] = f"🎉 Won! Winner is {win}. +₹{pz}"
            else: db["msg"] = f"😢 Lost! Winner was {win}."
        else: db["msg"] = f"Round end. Winner: {win}"
        db["color"] = None; db["bet_amt"] = 0.0
        return jsonify({"bal": db["bal"], "msg": db["msg"]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
        
