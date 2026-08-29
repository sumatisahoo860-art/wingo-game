import tkinter as tk
from tkinter import messagebox
import random

# Demo account
DEMO_ID = "demo123"
DEMO_PASSWORD = "1234"

period = 100001
history = []

def login():
    if id_entry.get() == DEMO_ID and pass_entry.get() == DEMO_PASSWORD:
        login_frame.pack_forget()
        game_frame.pack(fill="both", expand=True)
        update_period()
    else:
        messagebox.showerror("Login Failed", "Demo ID या Password गलत है")

def update_period():
    period_label.config(text=f"Period Number: {period}")

def play(color):
    global period

    result = random.choice(["RED", "GREEN", "VIOLET"])

    if color == result:
        status = "WIN"
    else:
        status = "LOSS"

    history.insert(0, f"Period {period} | Selected: {color} | Result: {result} | {status}")

    history_box.delete(0, tk.END)
    for item in history[:10]:
        history_box.insert(tk.END, item)

    result_label.config(text=f"Result: {result}   ({status})")

    period += 1
    update_period()


# ---------------- WINDOW ----------------

root = tk.Tk()
root.title("Demo Colour Game")
root.geometry("420x600")
root.resizable(False, False)

# ---------------- LOGIN ----------------

login_frame = tk.Frame(root)
login_frame.pack(fill="both", expand=True)

tk.Label(
    login_frame,
    text="DEMO LOGIN",
    font=("Arial", 24, "bold")
).pack(pady=50)

tk.Label(login_frame, text="Login ID").pack()
id_entry = tk.Entry(login_frame, width=30)
id_entry.pack(pady=8)

tk.Label(login_frame, text="Password").pack()
pass_entry = tk.Entry(login_frame, width=30, show="*")
pass_entry.pack(pady=8)

tk.Button(
    login_frame,
    text="LOGIN",
    width=20,
    command=login
).pack(pady=25)

tk.Label(
    login_frame,
    text="Demo ID: demo123\nPassword: 1234",
    fg="gray"
).pack()


# ---------------- GAME ----------------

game_frame = tk.Frame(root)

tk.Label(
    game_frame,
    text="COLOUR GAME",
    font=("Arial", 24, "bold")
).pack(pady=20)

period_label = tk.Label(
    game_frame,
    text="Period Number: 100001",
    font=("Arial", 16, "bold")
)
period_label.pack(pady=10)

tk.Label(
    game_frame,
    text="Select Colour",
    font=("Arial", 14)
).pack(pady=15)

tk.Button(
    game_frame,
    text="RED",
    width=20,
    command=lambda: play("RED")
).pack(pady=6)

tk.Button(
    game_frame,
    text="GREEN",
    width=20,
    command=lambda: play("GREEN")
).pack(pady=6)

tk.Button(
    game_frame,
    text="VIOLET",
    width=20,
    command=lambda: play("VIOLET")
).pack(pady=6)

result_label = tk.Label(
    game_frame,
    text="Result: ---",
    font=("Arial", 16, "bold")
)
result_label.pack(pady=25)

tk.Label(
    game_frame,
    text="History",
    font=("Arial", 14, "bold")
).pack()

history_box = tk.Listbox(
    game_frame,
    width=55,
    height=10
)
history_box.pack(pady=10)

tk.Label(
    game_frame,
    text="DEMO ONLY • No real money",
    fg="gray"
).pack(pady=10)

root.mainloop()
