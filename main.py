from flask import Flask, request, redirect, session, render_template_string
import random

app = Flask(__name__)
app.secret_key = "demo-secret-key"

DEMO_ID = "demo123"
DEMO_PASSWORD = "1234"

period = 100001
history = []

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Demo Colour Game</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial;
            background: #f2f2f2;
            text-align: center;
            padding: 25px;
        }
        .box {
            max-width: 400px;
            margin: auto;
            background: white;
            padding: 25px;
            border-radius: 15px;
        }
        input, button {
            width: 90%;
            padding: 12px;
            margin: 8px;
            border-radius: 8px;
            border: 1px solid #ccc;
        }
        button {
            cursor: pointer;
            font-weight: bold;
        }
        .history {
            text-align: left;
            font-size: 13px;
        }
    </style>
</head>
<body>
<div class="box">

{% if page == "login" %}

<h1>Demo Login</h1>

<form method="POST">
    <input name="user_id" placeholder="Login ID" required>
    <input name="password" type="password" placeholder="Password" required>
    <button type="submit">LOGIN</button>
</form>

<p>Demo ID: <b>demo123</b></p>
<p>Password: <b>1234</b></p>

{% else %}

<h1>Colour Game</h1>

<h3>Period Number: {{ period }}</h3>

<form method="POST" action="/play">
    <button name="color" value="RED">RED</button>
    <button name="color" value="GREEN">GREEN</button>
    <button name="color" value="VIOLET">VIOLET</button>
</form>

{% if result %}
<h2>Result: {{ result }}</h2>
<p>{{ status }}</p>
{% endif %}

<hr>

<h3>History</h3>

<div class="history">
{% for item in history %}
<p>{{ item }}</p>
{% endfor %}
</div>

<p>DEMO ONLY — No real money</p>

{% endif %}

</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_id = request.form.get("user_id")
        password = request.form.get("password")

        if user_id == DEMO_ID and password == DEMO_PASSWORD:
            session["login"] = True
            return redirect("/game")

        return "Login Failed. Use demo123 / 1234"

    return render_template_string(HTML, page="login")


@app.route("/game")
def game():
    if not session.get("login"):
        return redirect("/")

    return render_template_string(
        HTML,
        page="game",
        period=period,
        history=history,
        result=None,
        status=""
    )


@app.route("/play", methods=["POST"])
def play():
    global period

    if not session.get("login"):
        return redirect("/")

    selected = request.form.get("color")
    result = random.choice(["RED", "GREEN", "VIOLET"])

    status = "WIN" if selected == result else "LOSS"

    history.insert(
        0,
        f"Period {period} | Selected: {selected} | Result: {result} | {status}"
    )

    period += 1

    return render_template_string(
        HTML,
        page="game",
        period=period,
        history=history[:10],
        result=result,
        status=status
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
