from flask import Flask, jsonify, render_template
from flask_cors import CORS
import requests
import threading
import time
from ai_engine import ai_engine

app = Flask(__name__)
CORS(app)

# ======================
# GLOBAL STATE (REAL DATA)
# ======================
prices = []
last_update_time = 0


# ======================
# BINANCE PRICE FEED (REAL)
# ======================
def price_loop():
    global prices

    while True:
        try:
            url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m&limit=100"
            data = requests.get(url, timeout=5).json()

            new_prices = []

            for c in data:
                close_price = float(c[4])
                new_prices.append(close_price)

            prices = new_prices

        except Exception as e:
            print("Price fetch error:", e)

        time.sleep(10)  # update every 10 sec


# start thread
threading.Thread(target=price_loop, daemon=True).start()


# ======================
# ROUTES
# ======================
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/signal")
def signal():
    return jsonify(ai_engine(prices))


@app.route("/api/history")
def history():
    return jsonify(prices[-100:])


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


@app.route("/debug")
def debug():
    return {
        "price_count": len(prices),
        "last_price": prices[-1] if prices else 0
    }


# ======================
# RUN
# ======================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
