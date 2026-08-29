from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>SixPay Demo</title>
    <style>
        body {
            font-family: Arial;
            background: #f2f4f7;
            text-align: center;
            padding: 40px;
        }
        .box {
            max-width: 400px;
            margin: auto;
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 4px 15px #ccc;
        }
        input, button {
            width: 90%;
            padding: 12px;
            margin: 10px;
            border-radius: 8px;
            border: 1px solid #ccc;
        }
        button {
            background: #1677ff;
            color: white;
            border: none;
            cursor: pointer;
        }
    </style>
</head>
<body>
<div class="box">
    <h1>SixPay</h1>
    <p>Wallet Balance: ₹{{ balance }}</p>

    <form method="POST">
        <input type="number" name="amount"
               placeholder="Enter amount" min="1" required>
        <button type="submit">Pay</button>
    </form>

    {% if message %}
        <h3>{{ message }}</h3>
    {% endif %}
</div>
</body>
</html>
"""

balance = 1000

@app.route("/", methods=["GET", "POST"])
def home():
    global balance
    message = ""

    if request.method == "POST":
        amount = float(request.form["amount"])

        if amount <= balance:
            balance -= amount
            message = f"Demo payment successful: ₹{amount:.2f}"
        else:
            message = "Insufficient demo balance!"

    return render_template_string(
        HTML,
        balance=f"{balance:.2f}",
        message=message
    )

if __name__ == "__main__":
    app.run(debug=True)
