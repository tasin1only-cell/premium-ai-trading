from flask import Flask, jsonify, request
import random
import math

app = Flask(__name__)

# ======================
# SIMPLE MARKET SIM (replace later with real API)
# ======================
price = 100.0

history = [100 + random.uniform(-1, 1) for _ in range(50)]


# ======================
# RSI CALC
# ======================
def rsi(data):
    gain = 0
    loss = 0

    for i in range(1, len(data)):
        diff = data[i] - data[i-1]
        if diff > 0:
            gain += diff
        else:
            loss += abs(diff)

    rs = gain / (loss or 1)
    return 100 - (100 / (1 + rs))


# ======================
# TREND
# ======================
def trend(data):
    if len(data) < 10:
        return "SIDE"

    if data[-1] > data[-10]:
        return "UP"
    elif data[-1] < data[-10]:
        return "DOWN"
    return "SIDE"


# ======================
# AI ENGINE v3
# ======================
def ai_engine(data):

    t = trend(data)
    r = rsi(data)

    signal = "WAIT"
    confidence = 50

    if t == "UP" and r < 70:
        signal = "BUY"
        confidence = 75 + random.randint(0, 20)

    elif t == "DOWN" and r > 30:
        signal = "SELL"
        confidence = 75 + random.randint(0, 20)

    else:
        signal = "WAIT"
        confidence = 40 + random.randint(0, 15)

    return {
        "trend": t,
        "rsi": round(r, 2),
        "signal": signal,
        "confidence": confidence,
        "price": data[-1]
    }


# ======================
# UPDATE MARKET
# ======================
def update_price():
    global history
    move = random.uniform(-1.5, 1.5)
    new_price = history[-1] + move
    history.append(new_price)
    if len(history) > 100:
        history.pop(0)


# ======================
# API
# ======================
@app.route("/api/signal")
def get_signal():
    update_price()
    return jsonify(ai_engine(history))


@app.route("/api/history")
def get_history():
    return jsonify(history)


if __name__ == "__main__":
    app.run(debug=True)
