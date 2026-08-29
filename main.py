from flask import Flask, render_template_string, request
import random

app = Flask(__name__)

balance = 10000  # virtual demo points

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Colour Prediction - Demo</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial;
            background: #f3f4f6;
            text-align: center;
            padding: 20px;
        }
        .box {
            max-width: 400px;
            margin: auto;
            background: white;
            padding: 25px;
            border-radius: 18px;
            box-shadow: 0 4px 15px #ccc;
        }
        button {
            padding: 14px 25px;
            margin: 7px;
            border: 0;
            border-radius: 10px;
            color: white;
            font-size: 17px;
        }
        .red { background: #e53935; }
        .green { background: #2e9d50; }
        .blue { background: #1976d2; }
    </style>
</head>
<body>
<div class="box">
    <h1>Colour Demo</h1>
    <h2>Virtual Balance: {{ balance }} points</h2>

    <form method="POST">
        <p>Select a colour:</p>
        <button class="red" name="colour" value="Red">Red</button>
        <button class="green" name="colour" value="Green">Green</button>
        <button class="blue" name="colour" value="Blue">Blue</button>
    </form>

    {% if result %}
        <hr>
        <h2>Result: {{ result }}</h2>
        <h3>{{ message }}</h3>
    {% endif %}

    <p>This is a virtual-points demo only.</p>
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    global balance

    result = ""
    message = ""

    if request.method == "POST":
        selected = request.form["colour"]
        result = random.choice(["Red", "Green", "Blue"])

        if selected == result:
            balance += 100
            message = "Demo points +100 🎉"
        else:
            balance -= 100
            message = "Demo points -100"

    return render_template_string(
        HTML,
        balance=balance,
        result=result,
        message=message
    )

if __name__ == "__main__":
    import os
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
