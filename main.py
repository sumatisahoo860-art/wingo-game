import random
import os
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# ग्लोबल डेटाबेस स्टेट
db = {
    "user": "admin",
    "bal": 1000.0,
    "msg": "अपनी बेट राशि दर्ज करें और प्रेडिक्शन चुनें!",
    "hist": ["Red", "Green", "Violet", "Green", "Red"],
    "color": None,
    "bet_amt": 0.0,
    "pid": 2026083001
}

# कंबाइंड प्रीमियम फ्रंटエンド सिस्टम (लॉगिन -> डैशबोर्ड -> गेम)
html_code = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>51Game Premium Platform</title>
    <style>
        * { margin:0; padding:0; box-sizing:border-box; font-family:sans-serif; }
        body { background:#1a1a24; color:#fff; display:flex; justify-content:center; padding:15px; }
        .box { width:100%; max-width:430px; background:#222232; border-radius:20px; padding:20px; text-align:center; min-height:85vh; }
        .card { background:linear-gradient(135deg, #2b5876, #4e4376); border-radius:15px; padding:20px; margin:15px 0; }
        input { width:100%; padding:12px; background:rgba(255,255,255,0.08); border:1px solid #3a3a52; border-radius:8px; color:#fff; margin-bottom:15px; outline:none; text-align:center; font-size:16px; }
        button { width:100%; padding:12px; background:linear-gradient(90deg, #ff416c, #ff4b2b); border:none; border-radius:8px; color:#fff; font-weight:bold; cursor:pointer; }
        .grid { display:grid; grid-template-columns:1fr 1fr; gap:15px; margin-top:20px; }
        .g-card { background:#1f1f1f; padding:20px; border-radius:10px; border:1px solid #333; text-align:center; cursor:pointer; }
        .play-btn { background:#ff4b2b; color:#fff; font-size:12px; padding:6px 12px; border-radius:5px; display:inline-block; margin-top:10px; font-weight:bold; }
        .c-btns { display:flex; gap:10px; margin-bottom:15px; }
        .cb { flex:1; padding:12px 5px; border:none; border-radius:10px; font-weight:bold; color:#fff; font-size:15px; }
        .bg { background:#00b0ff; } .bv { background:#9c27b0; } .br { background:#ff3b30; }
        .cb:disabled { background:#555 !important; cursor:not-allowed; opacity:0.6; }
        .status { background:#1a1a24; padding:12px; border-radius:12px; margin-bottom:15px; border-left:4px solid #ffdf00; font-size:14px; text-align:left; }
        .dots { display:flex; gap:8px; justify-content:center; margin-top:8px; }
        .dot { width:32px; height:32px; border-radius:50%; display:flex; justify-content:center; align-items:center; font-size:10px; font-weight:bold; }
        .dot-Green { background:#00b0ff; } .dot-Red { background:#ff3b30; } .dot-Violet { background:#9c27b0; }
    </style>
</head><body>

<!-- १. लॉगिन स्क्रीन -->
<div id="p-login" class="box">
    <br><h2>👑 51Game Login</h2><br><br>
    <input type="text" id="u" placeholder="Username (admin)">
    <input type="password" id="p" placeholder="Password (1245)">
    <button onclick="doLogin()">SECURE LOGIN</button>
</div>

<!-- २. मुख्य डैशबोर्ड स्क्रीन -->
<div id="p-dash" class="box" style="display:none;">
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <h3>ID: admin ✨</h3><span onclick="logout()" style="color:#ff3b30; cursor:pointer; font-weight:bold; font-size:14px;">Logout</span>
    </div>
    <div class="card">
        <h3>AVAILABLE BALANCE</h3>
        <p id="d-bal" style="font-size:32px; font-weight:bold; margin-top:5px; color:#ffdf00;">₹ 1000.00</p>
        <button onclick="deposit()" style="background:#ffdf00; color:#000; width:auto; padding:6px 15px; border-radius:20px; margin-top:10px; font-weight:bold; border:none; cursor:pointer;">💰 Quick Deposit (+₹500)</button>
    </div>
    <h3 style="text-align:left; color:#ff416c; margin-top:20px;">🎯 Popular Games</h3>
    <div class="grid">
        <div class="g-card" onclick="goGame()">
            <h4>Win Go</h4><p style="font-size:11px; color:#aaa;">Color Prediction 1M</p>
            <span class="play-btn">Play Now</span>
        </div>
        <div class="g-card" style="opacity:0.5; cursor:not-allowed;">
            <h4>Aviator</h4><p style="font-size:11px; color:#aaa;">Crash Game</p>
            <span class="play-btn" style="background:#555;">Locked</span>
        </div>
    </div>
</div>

<!-- ३. ऑटो-टाइमर Win Go गेम स्क्रीन -->
<div id="p-game" class="box" style="display:none;">
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <button onclick="goDash()" style="width:auto; padding:5px 12px; background:#ffdf00; color:#000; font-weight:bold; border:none; border-radius:5px; cursor:pointer;">⬅ Dashboard</button>
        <span>Win Go 1Min</span>
    </div>
    <div class="card">
        <h3>AVAILABLE BALANCE</h3>
        <div id="g-bal" style="font-size:32px; font-weight:bold; margin-top:5px; color:#ffdf00;">₹ 1000.00</div>
    </div>
    <div style="display:flex; justify-content:space-between; background:#2a2a3e; padding:12px; border-radius:12px; margin-bottom:15px;">
        <div style="text-align:left;"><b style="color:#00ffcc;">🎯 Auto Processing</b><br><span id="l-msg" style="font-size:11px; color:#aaa;">प्रेडिक्शन खुला है!</span></div>
        <div id="count" style="font-size:24px; font-weight:bold; color:#00ffcc;">00:30</div>
    </div>
    <label style="font-size:12px; color:#aaa; display:block; text-align:left; margin-bottom:5px;">💵 अपनी बेट राशि दर्ज करें (Real Amount):</label>
    <input type="number" id="b-amount" value="100" min="10">
    <div class="c-btns">
        <button id="btn-Green" onclick="bet('Green')" class="cb bg">Green (2x)</button>
        <button id="btn-Violet" onclick="bet('Violet')" class="cb bv">Violet (3x)</button>
        <button id="btn-Red" onclick="bet('Red')" class="cb br">Red (2x)</button>
    </div>
    <div class="status"><strong>Status:</strong> <span id="st-txt">राशि सेट करें और रंग चुनें।</span></div>
    <div style="background:#2a2a3e; padding:15px; border-radius:12px;">
        <span style="font-size:13px; color:#aaa; display:block; text-align:left; margin-bottom:5px;">📊 Recent Trends (Period: <span id="pid">2026083001</span>)</span>
        <div class="dots" id="hist-box"></div>
    </div>
</div>

<script>
    let time = 30;
    function show(id) { ['p-login','p-dash','p-game'].forEach(p=>document.getElementById(p).style.display=p===id?'block':'none'); }
    function doLogin() {
        if(document.getElementById('u').value==='admin' && document.getElementById('p').value==='1245') { show('p-dash'); } 
        else { alert("गलत क्रेडेंशियल्स! admin और 1245 दर्ज करें।"); }
    }
    function goGame() { show('p-game'); updateHistory(); }
    function goDash() { show('p-dash'); }
    function logout() { show('p-login'); document.getElementById('u').value=''; document.getElementById('p').value=''; }
    
    function deposit() {
        fetch('/api/action', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({action:'deposit'})})
        .then(r=>r.json()).then(d=>{ updateUI(d); alert("₹500 जमा हो गए!"); });
    }
    function bet(color) {
        if(time <= 5) return;
        let amt = parseFloat(document.getElementById('b-amount').value);
        if(isNaN(amt) || amt <= 0) { alert("कृपया सही राशि दर्ज करें!"); return; }
        fetch('/api/action', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({action:'bet', color:color, amount:amt})})
        .then(r=>r.json()).then(d=>{
            if(d.status==='success'){ updateUI(d); document.getElementById('st-txt').innerText="आपने " + color + " पर ₹" + amt + " की बेट लॉक कर दी है।"; }
            else { alert(d.msg); }
        });
    }
    function updateUI(d) {
        document.getElementById('d-bal').innerText = "₹ " + d.bal.toFixed(2);
        document.getElementById('g-bal').innerText = "₹ " + d.bal.toFixed(2);
    }
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
            ['Green','Violet','Red'].forEach(c=>document.getElementById('btn-'+c).disabled=false);
            document.getElementById('b-amount').disabled = false;
            document.getElementById('l-msg').innerText = "प्रेडिक्शन खुला है!";
            document.getElementById('count').style.color = '#00ffcc';
        }
        document.getElementById('count').innerText = `00:${time<10?'0'+time:time}`;
        if(time <= 5 && time > 0) {
            ['Green','Violet','Red'].forEach(c=>document.getElementById('btn-'+c).disabled=true);
            document.getElementById('b-amount').disabled = true;
            document.getElementById('l-msg').innerText = "🛑 बेटिंग बंद (Locked)!";
            document.getElementById('count').style.color = '#ff3b30';
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
            
