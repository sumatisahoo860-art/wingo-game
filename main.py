import time
import random
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List

app = FastAPI(title="Safe Wingo Color Game API")

# Global Game State
game_state = {
    "period_id": 20260901001,
    "timer": 30,  # 30 seconds game cycle
    "next_result_override": None,  # Admin override parameter
    "history": []
}

# Dummy User Database (In-Memory)
users_db: Dict[str, dict] = {
    "user123": {"username": "player1", "coins": 10000} # Users start with 10k free coins
}

# Current Active Bets
active_bets: List[dict] = []

class BetModel(BaseModel):
    user_id: str
    chosen_color: str  # "red", "green", "violet"
    amount: int

class OverrideModel(BaseModel):
    secret_admin_key: str
    target_color: str

# 1. Fetch Game Status & Timer
@app.get("/game/status")
def get_game_status():
    return {
        "period_id": game_state["period_id"],
        "timer": game_state["timer"],
        "history": game_state["history"][-10:] # Show last 10 results
    }

# 2. Fetch User Coin Balance
@app.get("/user/balance/{user_id}")
def get_balance(user_id: str):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return {"coins": users_db[user_id]["coins"]}

# 3. Place a Bet (Virtual Coins)
@app.post("/game/bet")
def place_bet(bet: BetModel):
    if bet.user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = users_db[bet.user_id]
    if user["coins"] < bet.amount:
        raise HTTPException(status_code=400, detail="Insufficient virtual coins")
    
    if bet.chosen_color not in ["red", "green", "violet"]:
        raise HTTPException(status_code=400, detail="Invalid color choice")

    # Deduct coins and record bet
    user["coins"] -= bet.amount
    active_bets.append({
        "user_id": bet.user_id,
        "chosen_color": bet.chosen_color,
        "amount": bet.amount
    })
    return {"status": "Bet successfully placed!", "remaining_coins": user["coins"]}

# 4. Admin Control Panel (Result Changer)
@app.post("/admin/override")
def admin_override(data: OverrideModel):
    # Protect with a basic key
    if data.secret_admin_key != "MY_SUPER_SECRET_KEY_123":
        raise HTTPException(status_code=403, detail="Unauthorized Admin")
    
    if data.target_color not in ["red", "green", "violet"]:
        raise HTTPException(status_code=400, detail="Invalid color")
        
    game_state["next_result_override"] = data.target_color
    return {"status": f"Success! Next winning color forced to: {data.target_color}"}

# Background Logic simulator to settle bets every 30 seconds
# Note: In production, run this in a separate background thread / task loop
def settle_game_round():
    global active_bets
    
    # Determine Winner
    if game_state["next_result_override"]:
        winning_color = game_state["next_result_override"]
        game_state["next_result_override"] = None # Reset override
    else:
        # Standard Random if admin doesn't interfere
        winning_color = random.choice(["red", "green", "violet"])
    
    # Process all bets
    for bet in active_bets:
        user = users_db[bet["user_id"]]
        if bet["chosen_color"] == winning_color:
            # Win payout multipliers
            multiplier = 2 if winning_color in ["red", "green"] else 4.5
            winnings = int(bet["amount"] * multiplier)
            user["coins"] += winnings

    # Save to history & update period
    game_state["history"].append({"period_id": game_state["period_id"], "winner": winning_color})
    game_state["period_id"] += 1
    active_bets = [] # Clear active bets for next round
