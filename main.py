from flask import Flask, render_template_string, request

app = Flask(__name__)

balance = 1000

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>SixPay Demo</title>
</head>
<body>
    <h1>SixPay</h1>
    <h2>Balance: ₹{{ balance }}</h2>

    <form method="POST">
        <input type="number" name="amount" min="1" required>
        <button type="submit">Pay</button>
    </form>

    <p>{{ message }}</p>
</body>
</html>
"""

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
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
