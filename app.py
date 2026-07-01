from flask import Flask, jsonify, render_template
from flask_cors import CORS
import threading
import time
import random
import requests
from ai_engine import ai_engine   # ✅ FIXED IMPORT

app = Flask(__name__)
CORS(app)

# ======================
# GLOBAL STATE
# ======================
prices = []
last_signal_time = 0


# ======================
# PRICE FEED
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
# REAL CANDLES (BINANCE)
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
# ROUTES
# ======================
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/signal")
def signal():
    result = ai_engine(prices)
    return jsonify(result)


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
