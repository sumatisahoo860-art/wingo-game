import asyncio
import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# गेम स्टेट स्टोर करने के लिए
game_state = {
    "time_left": 30,
    "winning_colour": "None",
    "round_id": 10001
}

colours = ["Green", "Red", "Violet"]

# रीयल-टाइम बैकग्राउंड टाइमर लूप
async def game_timer_loop():
    global game_state
    while True:
        try:
            if game_state["time_left"] <= 0:
                game_state["winning_colour"] = random.choice(colours)
                game_state["round_id"] += 1
                game_state["time_left"] = 30
            else:
                game_state["time_left"] -= 1
            await asyncio.sleep(1)
        except Exception as e:
            print(f"Error in timer loop: {e}")
            await asyncio.sleep(1)

# लाइफसाइकिल मैनेजर - यह सर्वर शुरू होते ही टाइमर को बैकग्राउंड में चालू कर देता है
@asynccontextmanager
async def lifespan(app: FastAPI):
    timer_task = asyncio.create_task(game_timer_loop())
    yield
    timer_task.cancel()

app = FastAPI(lifespan=lifespan)

# CORS एरर फिक्स करने के लिए
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "success", "message": "Wingo Python Server is Running Perfectly!"}

@app.get("/api/game-state")
def get_game_state():
    return game_state
    
