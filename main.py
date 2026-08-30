import asyncio
import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

app = FastAPI()

# Render पर CORS एरर से बचने के लिए कॉन्फ़िगरेशन
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# गेम स्टेट वैरिएबल्स
game_state = {
    "time_left": 30,
    "winning_colour": "None",
    "round_id": 10001
}

colours = ["Green", "Red", "Violet"]

# रीयल-टाइम बैकग्राउंड टाइमर लूप (जो सर्वर पर लगातार बैकग्राउंड में चलेगा)
async def game_timer_loop():
    global game_state
    while True:
        if game_state["time_left"] <= 0:
            # रैंडम विनिंग कलर चुनना
            game_state["winning_colour"] = random.choice(colours)
            game_state["round_id"] += 1
            game_state["time_left"] = 30  # टाइमर रिसेट
            print(f"🎯 Round {game_state['round_id']} Result: {game_state['winning_colour']}")
        else:
            game_state["time_left"] -= 1
        
        await asyncio.sleep(1)

# सर्वर शुरू होते ही टाइमर लूप बैकग्राउंड में चालू हो जाएगा
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(game_timer_loop())

# होम रूट (यह चेक करने के लिए कि सर्वर लाइव है या नहीं)
@app.get("/")
def home():
    return {"status": "success", "message": "Wingo Python Backend is Running Successfully!"}

# फ्रंटएंड इस API को हर 1 सेकंड में कॉल करके लाइव टाइमर और रिजल्ट देख सकता है
@app.get("/api/game-state")
def get_game_state():
    return game_state

# 🔥 सबसे ज़रूरी फिक्स: Render द्वारा दिए गए PORT पर ही सर्वर बाइंड करना
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    # 0.0.0.0 पर बाइंड करना कंपल्सरी है ताकि बाहरी दुनिया से कनेक्शन मिल सके
    uvicorn.run("main.py:app", host="0.0.0.0", port=port, reload=False)
    
