from flask import Flask, jsonify, render_template
from flask_cors import CORS
import threading
import time
import random
from ai_engine import ai_engine

app = Flask(__name__)
CORS(app)

# ======================
# GLOBAL STATE
# ======================
prices = []

# ======================
# PRICE FEED (REAL SIMULATION)
# ======================
def price_loop():
    price = 100

    while True:
        price += random.uniform(-1.5, 1.5)
        prices.append(price)

        if len(prices) > 2000:
            prices.pop(0)

        time.sleep(1)

# ======================
# HOME
# ======================
@app.route("/")
def home():
    return render_template("index.html")

# ======================
# SIGNAL API
# ======================
@app.route("/api/signal")
def signal():
    return jsonify(ai_engine(prices))

# ======================
# HISTORY
# ======================
@app.route("/api/history")
def history():
    return jsonify(prices[-100:])

# ======================
# DEBUG
# ======================
@app.route("/debug")
def debug():
    return {
        "price_count": len(prices),
        "last_prices": prices[-5:]
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
