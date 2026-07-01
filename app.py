from flask import Flask, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# ======================
# MARKET DATA
# ======================
history = [100 + random.uniform(-1, 1) for _ in range(60)]


# ======================
# RSI CALCULATOR
# ======================
def calculate_rsi(data):
    gain = 0
    loss = 0

    for i in range(1, len(data)):
        diff = data[i] - data[i - 1]
        if diff > 0:
            gain += diff
        else:
            loss += abs(diff)

    rs = gain / (loss or 1)
    return 100 - (100 / (1 + rs))


# ======================
# TREND ENGINE
# ======================
def get_trend(data):
    if len(data) < 10:
        return "SIDE"

    if data[-1] > data[-10]:
        return "UP"
    elif data[-1] < data[-10]:
        return "DOWN"
    return "SIDE"


# ======================
# PRICE UPDATE ENGINE
# ======================
def update_price():
    global history

    change = random.uniform(-1.5, 1.5)
    new_price = history[-1] + change

    history.append(new_price)

    if len(history) > 100:
        history.pop(0)


# ======================
# AI BRAIN ENGINE (FIXED)
# ======================
def ai_engine(data):

    trend = get_trend(data)
    rsi = calculate_rsi(data)

    signal = "WAIT"
    confidence = 50

    # STRONG LOGIC
    if trend == "UP" and rsi < 70:
        signal = "BUY"
        confidence = 75 + random.randint(0, 20)

    elif trend == "DOWN" and rsi > 30:
        signal = "SELL"
        confidence = 75 + random.randint(0, 20)

    elif rsi < 25:
        signal = "STRONG BUY"
        confidence = 85 + random.randint(0, 10)

    elif rsi > 75:
        signal = "STRONG SELL"
        confidence = 85 + random.randint(0, 10)

    else:
        signal = "WAIT"
        confidence = 40 + random.randint(0, 15)

    # IMPORTANT: FIXED TYPES (NO STRING BUG)
    return {
        "trend": trend,
        "rsi": round(rsi, 2),
        "signal": signal,
        "confidence": int(confidence),
        "price": round(data[-1], 2)
    }


# ======================
# ROUTES
# ======================
@app.route("/")
def home():
    return "AI Trading Brain v3.1 Running ✔"


@app.route("/api/signal")
def get_signal():
    update_price()
    return jsonify(ai_engine(history))


@app.route("/api/history")
def get_history():
    return jsonify(history)


# ======================
# RUN SERVER
# ======================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
