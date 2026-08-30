import threading
import time
import random
import os
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

game_state = {
    "time_left": 30,
    "winning_colour": "None",
    "winning_number": 0,
    "round_id": 20260829100052663
}

colours = ["Green", "Red", "Violet"]

def game_timer_loop():
    global game_state
    while True:
        try:
            if game_state["time_left"] <= 0:
                # 0-9 रैंडम नंबर चुनना
                game_state["winning_number"] = random.randint(0, 9)
                num = game_state["winning_number"]
                
                # नंबर के आधार पर प्रोफेशनल कलर सेट करना
                if num == 0:
                    game_state["winning_colour"] = "Red+Violet"
                elif num == 5:
                    game_state["winning_colour"] = "Green+Violet"
                elif num % 2 == 0:
                    game_state["winning_colour"] = "Red"
                else:
                    game_state["winning_colour"] = "Green"
                    
                game_state["round_id"] += 1
                game_state["time_left"] = 30
            else:
                game_state["time_left"] -= 1
            time.sleep(1)
        except Exception:
            time.sleep(1)

timer_thread = threading.Thread(target=game_timer_loop, daemon=True)
timer_thread.start()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>51GAME Clone</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f5f5f5; color: #333; margin: 0; padding: 0; }
        .app-header { background: linear-gradient(135deg, #f1c40f, #f39c12); padding: 15px; text-align: center; color: white; font-weight: bold; font-size: 24px; position: relative; }
        .main-container { max-width: 450px; margin: 0 auto; background: #fff; min-height: 100vh; box-shadow: 0 0 10px rgba(0,0,0,0.1); padding-bottom: 50px; }
        
        .wallet-card { background: #fff; margin: 15px; padding: 20px; border-radius: 15px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.05); background: linear-gradient(to bottom, #fff7d6, #fff); border: 1px solid #ffe885; }
        .balance-title { font-size: 14px; color: #666; margin-bottom: 5px; }
        .balance-amount { font-size: 28px; font-weight: bold; color: #000; }
        .wallet-btns { display: flex; justify-content: space-around; margin-top: 15px; gap: 15px; }
        .w-btn { flex: 1; padding: 12px; border-radius: 25px; border: none; font-weight: bold; font-size: 16px; cursor: pointer; }
        .btn-withdraw { background: #ff4d4d; color: white; }
        .btn-deposit { background: #00b300; color: white; }
        
        .tabs-container { display: flex; background: #eee; margin: 15px; border-radius: 10px; padding: 5px; justify-content: space-between; }
        .tab-item { flex: 1; text-align: center; padding: 10px 0; font-size: 12px; color: #666; cursor: pointer; font-weight: bold; border-radius: 8px; }
        .tab-active { background: #f1c40f; color: white; }
        
        .timer-section { display: flex; justify-content: space-between; margin: 15px; background: #fffced; border: 1px dashed #f1c40f; padding: 15px; border-radius: 10px; align-items: center; }
        .timer-left h4 { margin: 0; color: #666; font-size: 14px; }
        .timer-left p { margin: 5px 0 0 0; font-weight: bold; color: #333; font-size: 13px; }
        .countdown-display { display: flex; gap: 5px; font-size: 24px; font-weight: bold; }
        .time-box { background: #000; color: #fff; padding: 5px 8px; border-radius: 5px; }
        .time-colon { color: #000; }

        .colour-row { display: flex; justify-content: space-between; margin: 15px; gap: 10px; }
        .c-btn { flex: 1; padding: 15px 0; border: none; border-radius: 8px; font-size: 16px; font-weight: bold; color: white; cursor: pointer; }
        .c-green { background: #00b300; }
        .c-violet { background: #bb33ff; }
        .c-red { background: #ff3333; }

        .numbers-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; margin: 15px; }
        .num-btn { width: 55px; height: 55px; border-radius: 50%; border: 2px solid #ddd; font-size: 18px; font-weight: bold; background: white; cursor: pointer; display: flex; align-items: center; justify-content: center; margin: 0 auto; }
        
        /* प्रोफेशनल 51Game कलर कोडिंग */
        .n0 { border-color: #bb33ff; color: #ff3333; background: linear-gradient(135deg, #ff3333 50%, #bb33ff 50%); color: white; }
        .n5 { border-color: #bb33ff; color: #00b300; background: linear-gradient(135deg, #00b300 50%, #bb33ff 50%); color: white; }
        .n1, .n3, .n7, .n9 { border-color: #00b300; color: #00b300; }
        .n2, .n4, .n6, .n8 { border-color: #ff3333; color: #ff3333; }

        .multiplier-row { display: flex; justify-content: space-between; margin: 15px; background: #f9f9f9; padding: 8px; border-radius: 8px; overflow-x: auto; gap: 5px; }
        .m-btn { padding: 6px 12px; border: 1px solid #ddd; background: white; border-radius: 15px; font-size: 12px; font-weight: bold; cursor: pointer; }
        .m-active { background: #00b300; color: white; border-color: #00b300; }

        .selection-panel { text-align: center; margin: 15px; font-weight: bold; color: #f39c12; font-size: 16px; background: #fffcf0; padding: 10px; border-radius: 8px; }
    </style>
</head>
<body>

<div class="main-container">
    <div class="app-header">51GAME</div>
    
    <div class="wallet-card">
        <div class="balance-title">Wallet balance</div>
        <div class="balance-amount">₹<span id="balance">0.25</span></div>
        <div class="wallet-btns">
            <button class="w-btn btn-withdraw">Withdraw</button>
            <button class="w-btn btn-deposit">Deposit</button>
        </div>
    </div>

    <div class="tabs-container">
        <div class="tab-item tab-active">WinGo 30sec</div>
        <div class="tab-item">WinGo 1 Min</div>
        <div class="tab-item">WinGo 3 Min</div>
        <div class="tab-item">WinGo 5 Min</div>
    </div>

    <div class="timer-section">
        <div class="timer-left">
            <h4>WinGo 30sec</h4>
            <p id="game-id">20260829100052663</p>
        </div>
        <div class="timer-right">
            <div style="font-size: 12px; color: #999; text-align: right; margin-bottom: 3px;">Time remaining</div>
            <div class="countdown-display">
                <span class="time-box">0</span>
                <span class="time-box">0</span>
                <span class="time-colon">:</span>
                <span class="time-box" id="t-sec1">0</span>
                <span class="time-box" id="t-sec2">0</span>
            </div>
        </div>
    </div>

    <div class="selection-panel">
        Selected: <span id="user-selection" style="color:#000;">None</span> <span id="m-text"></span>
    </div>

    <div class="colour-row">
        <button class="c-btn c-green" onclick="selectItem('Green')">Green</button>
        <button class="c-btn c-violet" onclick="selectItem('Violet')">Violet</button>
        <button class="c-btn c-red" onclick="selectItem('Red')">Red</button>
    </div>

    <div class="numbers-grid">
        <button class="num-btn n0" onclick="selectItem('0')">0</button>
        <button class="num-btn n1" onclick="selectItem('1')">1</button>
        <button class="num-btn n2" onclick="selectItem('2')">2</button>
        <button class="num-btn n3" onclick="selectItem('3')">3</button>
        <button class="num-btn n4" onclick="selectItem('4')">4</button>
        <button class="num-btn n5" onclick="selectItem('5')">5</button>
        <button class="num-btn n6" onclick="selectItem('6')">6</button>
        <button class="num-btn n7" onclick="selectItem('7')">7</button>
        <button class="num-btn n8" onclick="selectItem('8')">8</button>
        <button class="num-btn n9" onclick="selectItem('9')">9</button>
    </div>

    <div class="multiplier-row">
        <button class="m-btn m-active" onclick="setMult(1, this)">X1</button>
        <button class="m-btn" onclick="setMult(5, this)">X5</button>
        <button class="m-btn" onclick="setMult(10, this)">X10</button>
        <button class="m-btn" onclick="setMult(20, this)">X20</button>
        <button class="m-btn" onclick="setMult(50, this)">X50</button>
        <button class="m-btn" onclick="setMult(100, this)">X100</button>
    </div>
</div>

<script>
    let currentSelection = null;
    let multiplier = 1;
    let lastRoundId = null;

    function selectItem(val) {
        currentSelection = val;
        document.getElementById('user-selection').innerText = val;
        updateSelectionText();
    }

    function setMult(val, element) {
        multiplier = val;
        let buttons = document.querySelectorAll('.m-btn');
        buttons.forEach(b => b.classList.remove('m-active'));
        element.classList.add('m-active');
        updateSelectionText();
    }

    function updateSelectionText() {
        if(currentSelection !== null) {
            document.getElementById('m-text').innerText = " x" + multiplier;
        }
    }

    async function syncGame() {
        try {
            let response = await fetch('/api/game-state');
            let data = await response.json();
            
            // टाइमर को दो बॉक्स में बांटना (उदा: 25s -> 2 और 5)
            let seconds = data.time_left;
            let s1 = Math.floor(seconds / 10);
            let s2 = seconds % 10;
            document.getElementById('t-sec1').innerText = s1;
            document.getElementById('t-sec2').innerText = s2;
            
            document.getElementById('game-id').innerText = data.round_id;
            
            if (lastRoundId !== data.round_id) {
                if (lastRoundId !== null && currentSelection !== null) {
                    let isWin = false;

                    
