import random, os
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)
db = {"bal": 500.0, "msg": "प्रेडिक्शन चुनें!", "hist": ["Red", "Green"], "color": None, "bet_amt": 0.0, "pid": 101}

# १. लॉगिन और गेम का कंबाइंड लाइटवेट एचटीएमएल सिस्टम
html_code = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>51Game Live</title>
<style>
    body { background:#1a1a24; color:#fff; font-family:sans-serif; text-align:center; padding:15px; display:flex; justify-content:center; }
    .box { width:100%; max-width:420px; background:#222232; border-radius:20px; padding:20px; }
    .card { background:linear-gradient(135deg, #2b5876, #4e4376); border-radius:15px; padding:20px; margin:15px 0; }
    input { width:100%; padding:12px; background:rgba(255,255,255,0.1); border:none; border-radius:8px; color:#fff; margin-bottom:15px; outline:none; text-align:center; font-size:16px; }
    button { width:100%; padding:12px; background:linear-gradient(90deg, #ff416c, #ff4b2b); border:none; border-radius:8px; color:#fff; font-weight:bold; cursor:pointer; }
    .c-btns { display:flex; gap:10px; margin-bottom:15px; }
    .cb { flex:1; padding:12px 5px; border:none; border-radius:10px; font-weight:bold; color:#fff; font-size:15px; }
    .bg { background:#00b0ff; } .bv { background:#9c27b0; } .br { background:#ff3b30; }
    .cb:disabled { background:#555 !important; cursor:not-allowed; opacity:0.6; }
    .status { background:#1a1a24; padding:12px; border-radius:12px; margin-bottom:15px; border-left:4px solid #ffdf00; font-size:14px; text-align:left; }
    .dots { display:flex; gap:8px; justify-content:center; margin-top:8px; }
    .dot { width:35px; height:35px; border-radius:50%; display:flex; justify-content:center; align-items:center; font-size:10px; font-weight:bold; }
    .dot-Green { background:#00b0ff; } .dot-Red { background:#ff3b30; } .dot-Violet { background:#9c27b0; }
</style></head><body>

<!-- पहले यह लॉगिन स्क्रीन दिखेगी -->
<div id="p-login" class="box">
    <h2>51Game Login</h2><br>
    <input type="text" id="u" placeholder="Username (admin)">
    <input type="password" id="p" placeholder="Password (1245)">
    <button onclick="doLogin()">LOGIN</button>
</div>

<!-- लॉगिन के बाद यह गेम स्क्रीन खुलेगी -->
<div id="p-game" class="box" style="display:none;">
    <h2>🎯 Win Go 1Min (Live)</h2>
    <div class="card">
        <h3>AVAILABLE BALANCE</h3>
        <div id="bal" style="font-size:32px; font-weight:bold; margin-top:5px;">₹ 500.00</div>
        <button onclick="deposit()" style="background:#ffdf00; color:#000; width:auto; padding:6px 15px; border-radius:20px; margin-top:10px; font-weight:bold; border:none; cursor:pointer;">💰 Quick Deposit (+₹500)</button>
    </div>
    <div style="display:flex; justify-content:space-between; background:#2a2a3e; padding:12px; border-radius:12px; margin-bottom:15px;">
        <div style="text-align:left;"><b style="color:#00ffcc;">🎯 Auto Processing</b><br><span id="l-msg" style="font-size:11px; color:#aaa;">प्रेडिक्शन चुनें!</span></div>
        <div id="count" style="font-size:24px; font-weight:bold; color:#00ffcc;">00:30</div>
    </div>
    <input type="number" id="b-amount" value="100" min="10">
    <div class="c-btns">
        <button id="b-Green" onclick="bet('Green')" class="cb bg">Green (2x)</button>
        <button id="b-Violet" onclick="bet('Violet')" class="cb bv">Violet (3x)</button>
        <button id="b-Red" onclick="bet('Red')" class="cb br">Red (2x)</button>
    </div>
    <div class="status"><strong>Status:</strong> <span id="st-txt">राशि सेट करें और रंग चुनें।</span></div>
    <div style="background:#2a2a3e; padding:15px; border-radius:12px;">
        <span style="font-size:13px; color:#aaa;">📊 Trend History (Period: <span id="pid">101</span>)</span>
        <div class="dots" id="hist-box"></div>
    </div>
</div>

<script>
    let time = 30;
    function doLogin() {
        if(document.getElementById('u').value==='admin' && document.getElementById('p').value==='1245') {
            document.getElementById('p-login').style.display = 'none';
            document.getElementById('p-game').style.display = 'block';
            updateHistory();
        } else { alert("गलत यूजरनेम या पासवर्ड!"); }
    }
    function deposit() {
        fetch('/api/action', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({action:'deposit'})})
        .then(r=>r.json()).then(d=>{ updateUI(d); alert("₹500 जमा हो गए!"); });
    }
    function bet(color) {
        if(time <= 5) return;
        let amt = parseFloat(document.getElementById('b-amount').value);
        if(isNaN(amt) || amt <= 0) { alert("सही राशि दर्ज करें!"); return; }
        fetch('/api/action', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({action:'bet', color:color, amount:amt})})
        .then(r=>r.json()).then(d=>{
            if(d.status==='success'){ updateUI(d); document.getElementById('st-txt').innerText="आपने " + color + " पर ₹" + amt + " लगाए।"; }
            else { alert(d.msg); }
        });
    }
    function updateUI(d) { document.getElementById('bal').innerText = "₹ " + d.bal.toFixed(2); }
    function updateHistory() {
        fetch('/api/action', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({action:'get_state'})})
        .then(r=>r.json()).then(d=>{
            document.getElementById('pid').innerText = d.pid;
            let hHtml = ""; d.hist.forEach(c=>{ hHtml += `<div class="dot dot-${c}">${c}</div>`; });
            document.getElementById('hist-box').innerHTML = hHtml;
        });
    }
    setInterval(() => {
        time--;
        if(time < 0) {
            time = 30;
            ['Green','Violet','Red'].forEach(c=>document.getElementById('b-'+c).disabled=false);
            document.getElementById('b-amount').disabled = false;
            document.getElementById('l-msg').innerText = "प्रेडिक्शन चुनें!";
        }
        document.getElementById('count').innerText = `00:${time<10?'0'+time:time}`;
        if(time <= 5 && time > 0) {
            ['Green','Violet','Red'].forEach(c=>document.getElementById('b-'+c).disabled=true);
            document.getElementById('b-amount').disabled = true;
            document.getElementById('l-msg').innerText = "🛑 बेटिंग बंद (Locked)!";
        }
        if(time === 0) {
            fetch('/api/action', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({action:'result'})})
            .then(r=>r.json()).then(d=>{ updateUI(d); document.getElementById('st-txt').innerText = d.msg; updateHistory(); });
        }
    }, 1000);
</script>
</body></html>
"""

@app.route('/')
def home():
    return render_template_string(html_code)

@app.route('/api/action', methods=['POST'])
def api_action():
    act = request.json.get('action')
    if act == 'get_state': return jsonify(db)
    if act == 'deposit':
        db["bal"] += 500.0
        return jsonify({"bal": db["bal"]})
    if act == 'bet':
        amt = float(request.json.get('amount', 100.0))
        if db["bal"] >= amt:
            db["bal"] -= amt; db["color"] = request.json.get('color'); db["bet_amt"] = amt
            return jsonify({"status": "success", "bal": db["bal"]})
        return jsonify({"status": "error", "msg": "बैलेंस कम है!"})
    if act == 'result':
        win = random.choice(["Green", "Red", "Violet", "Green", "Red"])
        db["hist"].insert(0, win)
        if len(db["hist"]) > 5: db["hist"].pop()
        if db["color"]:
            mult = 3.0 if win == "Violet" else 2.0
            if db["color"] == win:
                prize = db["bet_amt"] * mult; db["bal"] += prize
                db["msg"] = f"🎉 जीत गए! विजेता रंग {win} है। मिले: ₹{prize:.2f}"
            else: db["msg"] = f"😢 हार गए! विजेता रंग {win} था। ₹{db['bet_amt']:.2f} नुकसान।"
        else: db["msg"] = f"⏱️ राउंड समाप्त! विजेता रंग {win} रहा।"
        db["pid"] += 1; db["color"] = None; db["bet_amt"] = 0.0
        return jsonify({"bal": db["bal"], "msg": db["msg"]})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
  
