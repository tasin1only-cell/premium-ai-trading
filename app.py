from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
import eventlet
import numpy as np
import random
import threading
import time

eventlet.monkey_patch()

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# ======================
# PRICE STORAGE
# ======================
prices = []


# ======================
# FAKE MARKET (SAFE FALLBACK)
# ======================
def fake_price_feed():
    base = 100
    noise = random.uniform(-2, 2)
    price = base + noise + random.uniform(0, 5)
    prices.append(price)

    if len(prices) > 500:
        prices.pop(0)


# ======================
# AI ENGINE (IMPROVED)
# ======================
def ai_engine(data):

    window = data[-30:]

    if len(window) < 10:
        window = data

    if len(window) == 0:
        return {
            "price": 0,
            "signal": "WAIT",
            "buy": 0.5,
            "sell": 0.5,
            "rsi": 50
        }

    momentum = window[-1] - window[0]
    volatility = np.std(window) if len(window) > 1 else 0
    mean_price = np.mean(window)

    buy = 50
    sell = 50

    # momentum influence
    buy += momentum * 4
    sell -= momentum * 4

    # volatility penalty
    if volatility > 1.5:
        buy -= 8
        sell -= 8

    # trend bias
    if window[-1] > mean_price:
        buy += 12
    else:
        sell += 12

    # decision engine
    if buy > sell + 5:
        signal = "BUY"
    elif sell > buy + 5:
        signal = "SELL"
    else:
        signal = "WAIT"

    rsi = 50 + (buy - sell)

    return {
        "price": round(window[-1], 2),
        "signal": signal,
        "buy": round(buy / 100, 2),
        "sell": round(sell / 100, 2),
        "rsi": round(rsi, 2)
    }


# ======================
# BACKGROUND LOOP (IMPORTANT)
# ======================
def price_loop():
    while True:
        fake_price_feed()
        time.sleep(2)


# ======================
# EMIT SIGNAL (SOCKET READY)
# ======================
def emit_signal():
    if len(prices) < 10:
        return

    data = ai_engine(prices)

    socketio.emit("update", {
        "price": data["price"],
        "signal": data["signal"],
        "confidence": round(data["buy"] * 100, 2),
        "trend": "UP" if data["signal"] == "BUY" else "DOWN",
        "rsi": data["rsi"]
    })


# ======================
# ROUTES
# ======================
@app.route("/")
def home():
    return "AI Trading Pro v5 Running ✔"


# ✅ MAIN FIXED API
@app.route("/api/signal")
def signal():

    if len(prices) < 5:
        return jsonify({
            "price": 0,
            "signal": "WAIT",
            "confidence": 50,
            "trend": "SIDE",
            "rsi": 50
        })

    data = ai_engine(prices)

    return jsonify({
        "price": data["price"],
        "signal": data["signal"],
        "confidence": round(data["buy"] * 100, 2),
        "trend": "UP" if data["signal"] == "BUY" else "DOWN",
        "rsi": data["rsi"]
    })


@app.route("/api/history")
def history():
    return jsonify(prices[-100:])


# ======================
# SOCKET
# ======================
@socketio.on("connect")
def connect():
    print("Client Connected ✔")


# ======================
# START SERVER
# ======================
if __name__ == "__main__":

    # start fake market
    threading.Thread(target=price_loop).start()

    socketio.run(app, host="0.0.0.0", port=10000)
