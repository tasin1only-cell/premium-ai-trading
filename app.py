from flask import Flask, jsonify
from flask_cors import CORS
import numpy as np
import threading
import time
import random

app = Flask(__name__)
CORS(app)

# ======================
# GLOBAL PRICE STORE
# ======================
prices = []


# ======================
# LIVE PRICE FEED (SIMULATED)
# ======================
def price_loop():
    price = 100

    while True:
        move = random.uniform(-1.2, 1.2)
        price += move

        prices.append(price)

        if len(prices) > 500:
            prices.pop(0)

        time.sleep(1.2)


# ======================
# EMA FUNCTION
# ======================
def ema(data, period):
    if len(data) < period:
        return np.mean(data) if data else 0

    alpha = 2 / (period + 1)
    result = data[0]

    for p in data:
        result = alpha * p + (1 - alpha) * result

    return result


# ======================
# RSI FUNCTION
# ======================
def rsi(data, period=14):
    if len(data) < period + 1:
        return 50

    gains = []
    losses = []

    for i in range(1, period + 1):
        diff = data[-i] - data[-i - 1]
        if diff > 0:
            gains.append(diff)
        else:
            losses.append(abs(diff))

    avg_gain = np.mean(gains) if gains else 0.01
    avg_loss = np.mean(losses) if losses else 0.01

    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


# ======================
# MACD FUNCTION
# ======================
def macd(data):
    ema12 = ema(data, 12)
    ema26 = ema(data, 26)
    return ema12 - ema26


# ======================
# AI ENGINE (FIXED & BALANCED)
# ======================
def ai_engine():

    if len(prices) < 20:
        return {
            "signal": "WAIT",
            "confidence": 50,
            "trend": "SIDE",
            "price": prices[-1] if prices else 0,
            "rsi": 50,
            "ema20": 0,
            "ema50": 0,
            "macd": 0
        }

    ema20 = ema(prices, 20)
    ema50 = ema(prices, 50)
    current_rsi = rsi(prices)
    current_macd = macd(prices)

    score = 0

    # ======================
    # EMA SIGNAL
    # ======================
    if ema20 > ema50:
        score += 35
    else:
        score -= 35

    # ======================
    # RSI SIGNAL
    # ======================
    if current_rsi < 45:
        score += 20
    elif current_rsi > 55:
        score -= 20

    # ======================
    # MACD SIGNAL
    # ======================
    if current_macd > 0:
        score += 25
    else:
        score -= 25

    # ======================
    # MOMENTUM (IMPORTANT FIX)
    # ======================
    if len(prices) > 10:
        momentum = prices[-1] - prices[-10]
        if momentum > 0.5:
            score += 20
        elif momentum < -0.5:
            score -= 20

    # ======================
    # DECISION ENGINE
    # ======================
    if score > 20:
        signal = "BUY"
        trend = "UP"
        confidence = min(95, 55 + abs(score))

    elif score < -20:
        signal = "SELL"
        trend = "DOWN"
        confidence = min(95, 55 + abs(score))

    else:
        signal = "WAIT"
        trend = "SIDE"
        confidence = 50 + abs(score) * 2

    return {
        "signal": signal,
        "confidence": round(confidence, 2),
        "trend": trend,
        "price": round(prices[-1], 2) if prices else 0,
        "rsi": round(current_rsi, 2),
        "ema20": round(ema20, 2),
        "ema50": round(ema50, 2),
        "macd": round(current_macd, 4)
    }


# ======================
# ROUTES
# ======================
@app.route("/")
def home():
    return "Level 6A FULL STABLE AI RUNNING ✔"


@app.route("/api/signal")
def signal():
    return jsonify(ai_engine())


@app.route("/api/history")
def history():
    return jsonify(prices[-100:])


@app.route("/debug")
def debug():
    return {
        "price_count": len(prices),
        "last_price": prices[-1] if prices else None
    }


# ======================
# START BACKGROUND THREAD
# ======================
threading.Thread(target=price_loop, daemon=True).start()


# ======================
# RUN SERVER
# ======================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
