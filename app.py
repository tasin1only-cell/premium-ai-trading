from flask import Flask, jsonify, render_template
from flask_cors import CORS
import numpy as np
import threading
import time
import random
import requests   # 🔥 NEW

app = Flask(__name__)
CORS(app)

# ======================
# GLOBAL STATE (LEVEL 6C)
# ======================
prices = []
last_signal_time = 0


# ======================
# PRICE FEED (YOUR SYSTEM)
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
# LEVEL 7: REAL CANDLE API
# ======================
@app.route("/api/candles")
def candles():
    try:
        url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m&limit=50"
        data = requests.get(url, timeout=5).json()

        candles = []
        for c in data:
            candles.append({
                "time": c[0],
                "open": float(c[1]),
                "high": float(c[2]),
                "low": float(c[3]),
                "close": float(c[4])
            })

        return jsonify(candles)

    except:
        return jsonify([])


# ======================
# EMA (SAFE)
# ======================
def ema(data, period):
    if len(data) < period:
        return data[-1] if data else 0

    alpha = 2 / (period + 1)
    result = np.mean(data[:period])

    for p in data[period:]:
        result = alpha * p + (1 - alpha) * result

    return result


# ======================
# RSI
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
# MACD
# ======================
def macd(data):
    if len(data) < 26:
        return 0

    ema12 = ema(data, 12)
    ema26 = ema(data, 26)

    return ema12 - ema26


# ======================
# AI ENGINE (UNCHANGED CORE)
# ======================
def ai_engine():
    global last_signal_time

    if len(prices) < 25:
        return {"signal": "WAIT", "confidence": 50, "trend": "SIDE", "price": 0}

    now = time.time()

    if now - last_signal_time < 60:
        return {
            "signal": "WAIT",
            "confidence": 50,
            "trend": "SIDE",
            "price": round(prices[-1], 2)
        }

    ema20 = ema(prices, 20)
    ema50 = ema(prices, 50)
    current_rsi = rsi(prices)
    current_macd = macd(prices)

    score = 0

    if ema20 > ema50:
        score += 25
    else:
        score -= 25

    if current_rsi < 45:
        score += 20
    elif current_rsi > 55:
        score -= 20

    if current_macd > 0.02:
        score += 20
    elif current_macd < -0.02:
        score -= 20

    momentum = prices[-1] - prices[-10]

    if momentum > 0.5:
        score += 15
    elif momentum < -0.5:
        score -= 15

    base_conf = 55 + abs(score)

    if score >= 45:
        signal = "BUY"
        confidence = min(92, base_conf)

    elif score <= -45:
        signal = "SELL"
        confidence = min(92, base_conf)

    else:
        signal = "WAIT"
        confidence = 50

    last_signal_time = now

    return {
        "signal": signal,
        "confidence": round(confidence, 2),
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


@app.route("/debug")
def debug():
    return {
        "price_count": len(prices),
        "last_prices": prices[-5:] if prices else []
    }


# ======================
# START THREAD
# ======================
threading.Thread(target=price_loop, daemon=True).start()


# ======================
# RUN
# ======================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
