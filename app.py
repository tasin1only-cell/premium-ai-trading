from flask import Flask, jsonify
from flask_cors import CORS
import random
import math

app = Flask(__name__)
CORS(app)

# ======================
# SIMULATED MARKET DATA
# ======================
prices = [100 + random.uniform(-1, 1) for _ in range(120)]


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


def ema(data, period=14):
    k = 2 / (period + 1)
    ema_val = data[0]

    for price in data:
        ema_val = price * k + ema_val * (1 - k)

    return ema_val


def volatility(data):
    mean = sum(data) / len(data)
    return sum((x - mean) ** 2 for x in data) / len(data)


# ======================
# PRICE UPDATE
# ======================
def update_price():
    global prices
    change = random.uniform(-1.5, 1.5)
    prices.append(prices[-1] + change)

    if len(prices) > 200:
        prices.pop(0)


# ======================
# FEATURE ENGINE
# ======================
def features(data):
    return {
        "rsi": rsi(data),
        "ema": ema(data),
        "price": data[-1],
        "volatility": volatility(data)
    }


# ======================
# PROBABILITY MODEL (LEVEL 2 CORE)
# ======================
def probability_engine(f):

    rsi_val = f["rsi"]
    ema_val = f["ema"]
    price = f["price"]
    vol = f["volatility"]

    # BASE SCORES
    buy = 0.5
    sell = 0.5

    # RSI influence
    if rsi_val < 30:
        buy += 0.25
    elif rsi_val > 70:
        sell += 0.25

    # EMA trend influence
    if price > ema_val:
        buy += 0.2
    else:
        sell += 0.2

    # Volatility adjustment
    if vol > 5:
        buy -= 0.05
        sell -= 0.05

    # Normalize
    total = buy + sell

    buy_prob = buy / total
    sell_prob = sell / total
    wait_prob = max(0, 1 - (buy_prob + sell_prob))

    return {
        "BUY": round(buy_prob, 2),
        "SELL": round(sell_prob, 2),
        "WAIT": round(wait_prob, 2)
    }


# ======================
# FINAL DECISION
# ======================
def decision(prob):

    if prob["BUY"] > 0.6:
        signal = "BUY"
    elif prob["SELL"] > 0.6:
        signal = "SELL"
    else:
        signal = "WAIT"

    confidence = max(prob["BUY"], prob["SELL"]) * 100

    return signal, int(confidence)


# ======================
# ROUTE
# ======================
@app.route("/api/signal")
def signal():

    update_price()

    f = features(prices)
    prob = probability_engine(f)
    signal, confidence = decision(prob)

    return jsonify({
        "trend": "UP" if prices[-1] > prices[-10] else "DOWN",
        "price": round(prices[-1], 2),
        "rsi": round(f["rsi"], 2),
        "ema": round(f["ema"], 2),
        "probability": prob,
        "signal": signal,
        "confidence": confidence
    })


@app.route("/api/history")
def history():
    return jsonify(prices)


# ======================
# RUN
# ======================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
