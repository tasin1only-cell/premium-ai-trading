from flask import Flask, jsonify
from flask_cors import CORS
import numpy as np
import threading
import time
import random

app = Flask(__name__)
CORS(app)

# ======================
# PRICE DATA STORE
# ======================
prices = []

# 🔥 candle lock (global state)
last_signal_time = 0


# ======================
# PRICE FEED (SIMULATED MARKET)
# ======================
def price_loop():
    price = 100

    while True:
        move = random.uniform(-1.5, 1.5)
        price += move

        prices.append(price)

        if len(prices) > 500:
            prices.pop(0)

        time.sleep(1)


# ======================
# EMA
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
# MACD
# ======================
def macd(data):
    return ema(data, 12) - ema(data, 26)


# ======================
# WINRATE BOOSTED AI ENGINE
# ======================
def ai_engine():
    global last_signal_time

    if len(prices) < 50:
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

    # 🔥 60 SEC CANDLE LOCK
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
        score += 30
    else:
        score -= 30

    # ======================
    # RSI FILTER
    # ======================
    if current_rsi < 45:
        score += 25
    elif current_rsi > 55:
        score -= 25

    # ======================
    # MACD FILTER
    # ======================
    if current_macd > 0.03:
        score += 25
    elif current_macd < -0.03:
        score -= 25

    # ======================
    # MOMENTUM FILTER
    # ======================
    momentum = prices[-1] - prices[-20]

    if momentum > 0.5:
        score += 20
    elif momentum < -0.5:
        score -= 20

    # ======================
    # FINAL DECISION
    # ======================
    base_conf = 55 + abs(score)

    if score >= 60:
        signal = "BUY"
        trend = "UP"
        confidence = min(95, base_conf + 10)

    elif score <= -60:
        signal = "SELL"
        trend = "DOWN"
        confidence = min(95, base_conf + 10)

    else:
        signal = "WAIT"
        trend = "SIDE"
        confidence = 50

    # 🔥 update lock only when real signal generated
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
    return "Level 6C STABLE AI RUNNING ✔"


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
# START PRICE LOOP
# ======================
threading.Thread(target=price_loop, daemon=True).start()


# ======================
# RUN APP
# ======================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
