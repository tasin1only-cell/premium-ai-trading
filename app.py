from flask import Flask, jsonify
from flask_cors import CORS
import numpy as np
import threading
import time
import random

app = Flask(__name__)
CORS(app)

# ======================
# PRICE STORAGE
# ======================
prices = []


# ======================
# PRICE FEED (SIMULATION / SAFE FOR RENDER)
# ======================
def price_loop():
    price = 100

    while True:
        move = random.uniform(-1.5, 1.5)
        price += move

        prices.append(price)

        if len(prices) > 500:
            prices.pop(0)

        time.sleep(1.5)


# ======================
# EMA
# ======================
def ema(data, period):
    if len(data) < period:
        return np.mean(data)

    alpha = 2 / (period + 1)
    result = data[0]

    for p in data:
        result = alpha * p + (1 - alpha) * result

    return result


# ======================
# RSI
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
# MACD (simple)
# ======================
def macd(data):
    ema12 = ema(data, 12)
    ema26 = ema(data, 26)
    return ema12 - ema26


# ======================
# AI ENGINE (FIXED LOGIC)
# ======================
def ai_engine():

    if len(prices) < 20:
        return {
            "signal": "WAIT",
            "confidence": 50,
            "trend": "SIDE",
            "price": 0,
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
    # EMA STRONG SIGNAL
    # ======================
    if ema20 > ema50:
        score += 40
    else:
        score -= 40

    # ======================
    # RSI BALANCED SIGNAL
    # ======================
    if current_rsi < 45:
        score += 25
    elif current_rsi > 55:
        score -= 25

    # ======================
    # MACD SIGNAL
    # ======================
    if current_macd > 0:
        score += 30
    else:
        score -= 30

    # ======================
    # DECISION ENGINE
    # ======================
    if score > 15:
        signal = "BUY"
        trend = "UP"
        confidence = min(95, 55 + abs(score))

    elif score < -15:
        signal = "SELL"
        trend = "DOWN"
        confidence = min(95, 55 + abs(score))

    else:
        trend = "SIDE"
        confidence = 50

        if len(prices) > 0 and prices[-1] > ema20:
            signal = "BUY"
        else:
            signal = "SELL"

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
    return "AI Trading Pro Level 6A FIXED RUNNING ✔"


@app.route("/api/signal")
def signal():
    return jsonify(ai_engine())


@app.route("/api/history")
def history():
    return jsonify(prices[-100:])


# ======================
# START BACKGROUND THREAD
# ======================
threading.Thread(target=price_loop, daemon=True).start()


# ======================
# RUN
# ======================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
