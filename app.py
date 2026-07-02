from flask import Flask, jsonify, render_template
from flask_cors import CORS
import threading
import time
import random
from ai_engine import ai_engine

app = Flask(__name__)
CORS(app)

prices = []

# ======================
# CANDLE BASED PRICE LOOP
# ======================
def price_loop():
    price = 100
    candle_buffer = []

    while True:
        price += random.uniform(-1.2, 1.2)
        candle_buffer.append(price)

        # 1 candle = 60 seconds
        if len(candle_buffer) >= 60:
            prices.append(candle_buffer[-1])  # CLOSE PRICE ONLY
            candle_buffer = []

        if len(prices) > 2000:
            prices.pop(0)

        time.sleep(1)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/signal")
def signal():
    return jsonify(ai_engine(prices))


@app.route("/api/history")
def history():
    return jsonify(prices[-100:])


@app.route("/debug")
def debug():
    return {
        "price_count": len(prices),
        "last_prices": prices[-5:]
    }


threading.Thread(target=price_loop, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
