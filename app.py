from flask import Flask, jsonify, render_template
from flask_cors import CORS
import threading
import time
import random
from ai_engine import ai_engine

app = Flask(__name__)
CORS(app)

prices = []

# 🔥 CANDLE STATE (IMPORTANT FIX)
candle_start = int(time.time() // 60)

def price_loop():
    price = 100

    while True:
        price += random.uniform(-1.2, 1.2)
        prices.append(price)

        if len(prices) > 2000:
            prices.pop(0)

        time.sleep(1)

@app.route("/")
def home():
    return render_template("index.html")

# 🔥 SIGNAL API (CANDLE SYNC ADDED)
@app.route("/api/signal")
def signal():
    global candle_start
    return jsonify({
        **ai_engine(prices),
        "candle_start": candle_start
    })

@app.route("/api/status")
def status():
    global candle_start

    new_candle = int(time.time() // 60)

    if new_candle != candle_start:
        candle_start = new_candle

    return jsonify({
        "candle_start": candle_start
    })

@app.route("/api/history")
def history():
    return jsonify(prices[-100:])

@app.route("/debug")
def debug():
    return {
        "price_count": len(prices),
        "last_prices": prices[-5:] if prices else []
    }

threading.Thread(target=price_loop, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
