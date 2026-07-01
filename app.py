from flask import Flask, jsonify, render_template
from flask_cors import CORS
import numpy as np
import threading
import time
import random

app = Flask(__name__)
CORS(app)

# ======================
# GLOBAL STATE
# ======================
prices = []
last_signal_time = 0


# ======================
# PRICE FEED (STABLE)
# ======================
def price_loop():
    price = 100

    while True:
        price += random.uniform(-1.3, 1.3)

        prices.append(price)

        if len(prices) > 1000:
            prices.pop(0)

        time.sleep(1)


# ======================
# SAFE EMA (FIXED VERSION)
# ======================
def ema(data, period):
    if len(data) < period:
        return data[-1] if data else 0

    alpha = 2 / (period + 1)

    # 🔥 FIX: proper initialization
    result = np.mean(data[:period])

    for p in data[period:]:
        result = alpha * p + (1 - alpha) * result

    return result


# ======================
# RSI (STABLE)
# ======================
def rsi(data, period=14):
    if len(data) < period + 2:
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
# MACD (SAFE)
# ======================
def macd(data):
    if len(data) < 26:
        return 0

    ema12 = ema(data, 12)
    ema26 = ema(data, 26)

    return ema12 - ema26


# ======================
# AI ENGINE (STABLE + FIXED)
# ======================
def ai_engine():
    global last_signal_time

    # 🔥 minimum data requirement FIXED
    if len(prices) < 25:
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

    now = time.time()

    # 🔥 60 sec candle lock
    if now - last_signal_time < 60:
        return {
            "signal": "WAIT",
            "confidence": 50,
            "trend": "SIDE",
            "price": round(prices[-1], 2),
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
    # TREND FILTER
    # ======================
    if ema20 > ema50:
        score += 25
    else:
        score -= 25

    # ======================
    # RSI FILTER
    # ======================
    if current_rsi < 45:
        score += 20
    elif current_rsi > 55:
        score -= 20

    # ======================
    # MACD FILTER
    # ======================
    if current_macd > 0.02:
        score += 20
    elif current_macd < -0.02:
        score -= 20

    # ======================
    # MOMENTUM
    # ======================
    momentum = prices[-1] - prices[-10]

    if momentum > 0.5:
        score += 15
    elif momentum < -0.5:
        score -= 15

    # ======================
    # FINAL DECISION
    # ======================
    base_conf = 55 + abs(score)

    if score >= 45:
        signal = "BUY"
        trend = "UP"
        confidence = min(92, base_conf)

    elif score <= -45:
        signal = "SELL"
        trend = "DOWN"
        confidence = min(92, base_conf)

    else:
        signal = "WAIT"
        trend = "SIDE"
        confidence = 50

    last_signal_time = now

    return {
        "signal": signal,
        "confidence": round(confidence, 2),
        "trend": trend,
        "price": round(prices[-1], 2),
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
    return render_template("index.html")


@app.route("/api/signal")
def signal():
    return jsonify(ai_engine())


@app.route("/api/history")
def history():
    return jsonify(prices[-100:])


# ======================
# DEBUG (VERY IMPORTANT)
# ======================
@app.route("/debug")
def debug():
    return {
        "price_count": len(prices),
        "last_prices": prices[-5:] if prices else []
    }


# ======================
# START PRICE FEED THREAD
# ======================
threading.Thread(target=price_loop, daemon=True).start()


# ======================
# RUN SERVER
# ======================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
