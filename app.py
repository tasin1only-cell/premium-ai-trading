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
# PRICE FEED (STABLE BOOT FIX)
# ======================
def price_loop():
    price = 100

    time.sleep(3)  # boot stabilization

    while True:
        price += random.uniform(-1.2, 1.2)
        prices.append(price)

        if len(prices) > 2000:
            prices.pop(0)

        time.sleep(1)

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

@app.route("/api/status")
def status():
    return {
        "price_count": len(prices),
        "last_price": prices[-1] if prices else 0,
        "server_time": time.time()
    }

@app.route("/debug")
def debug():
    return {
        "price_count": len(prices),
        "last_prices": prices[-5:] if prices else []
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
