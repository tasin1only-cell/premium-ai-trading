from flask import Flask, jsonify
from flask_cors import CORS
import random
import math

app = Flask(__name__)
CORS(app)

# ======================
# SIMULATED MARKET DATA
# ======================
prices = [100 + random.uniform(-1, 1) for _ in range(80)]


# ======================
# INDICATORS
# ======================
def rsi(data):
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


def ema(data, period=10):
    k = 2 / (period + 1)
    ema_val = data[0]

    for price in data:
        ema_val = price * k + ema_val * (1 - k)

    return ema_val


# ======================
# TREND ENGINE (IMPROVED)
# ======================
def trend(data):
    short = sum(data[-5:]) / 5
    long = sum(data[-20:]) / 20

    if short > long:
        return "UP"
    elif short < long:
        return "DOWN"
    return "SIDE"


# ======================
# PRICE UPDATE (SIMULATED)
# ======================
def update_price():
    global prices
    change = random.uniform(-1.2, 1.2)
    new_price = prices[-1] + change

    prices.append(new_price)

    if len(prices) > 120:
        prices.pop(0)


# ======================
# AI LOGIC (LEVEL 1 SMART)
# ======================
def ai_engine(data):

    current_rsi = rsi(data)
    current_ema = ema(data)
    current_price = data[-1]
    current_trend = trend(data)

    signal = "WAIT"
    confidence = 50

    # STRONG LOGIC (NO PURE RANDOM)
    if current_trend == "UP" and current_rsi < 70 and current_price > current_ema:
        signal = "BUY"
        confidence = int(75 + (70 - current_rsi) * 0.3)

    elif current_trend == "DOWN" and current_rsi > 30 and current_price < current_ema:
        signal = "SELL"
        confidence = int(75 + (current_rsi - 30) * 0.3)

    elif current_rsi < 25:
        signal = "STRONG BUY"
        confidence = 90

    elif current_rsi > 75:
        signal = "STRONG SELL"
        confidence = 90

    else:
        signal = "WAIT"
        confidence = 40 + random.randint(0, 10)

    return {
        "trend": current_trend,
        "rsi": round(current_rsi, 2),
        "ema": round(current_ema, 2),
        "price": round(current_price, 2),
        "signal": signal,
        "confidence": int(confidence)
    }


# ======================
# ROUTES
# ======================
@app.route("/")
def home():
    return "Level 1 AI Trading Engine Running ✔"


@app.route("/api/signal")
def signal():
    update_price()
    return jsonify(ai_engine(prices))


@app.route("/api/history")
def history():
    return jsonify(prices)


# ======================
# RUN
# ======================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
