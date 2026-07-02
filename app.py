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
signal_history = []

# ======================
# PRICE FEED (LEVEL 9 STABLE)
# ======================
def price_loop():
    price = 100

    while True:
        price += random.uniform(-1.5, 1.5)

        prices.append(price)

        if len(prices) > 3000:
            prices.pop(0)

        time.sleep(1)

# ======================
# HOME
# ======================
@app.route("/")
def home():
    return render_template("index.html")

# ======================
# SIGNAL API (LEVEL 9 HOOK)
# ======================
@app.route("/api/signal")
def signal():

    result = ai_engine(prices)

    # store history for analytics
    signal_history.append(result)

    if len(signal_history) > 500:
        signal_history.pop(0)

    return jsonify(result)

# ======================
# HISTORY (PRICE)
# ======================
@app.route("/api/history")
def history():
    return jsonify(prices[-100:])

# ======================
# SIGNAL HISTORY (NEW LEVEL 9)
# ======================
@app.route("/api/signal-history")
def signal_history_api():
    return jsonify(signal_history[-100:])

# ======================
# DEBUG
# ======================
@app.route("/debug")
def debug():
    return {
        "price_count": len(prices),
        "signal_count": len(signal_history),
        "last_prices": prices[-5:] if prices else []
    }

# ======================
# START THREAD (SAFE BOOT)
# ======================
threading.Thread(target=price_loop, daemon=True).start()

# ======================
# RUN
# ======================
if __name__ == "__main__":
    print("LEVEL 9 APP STARTED")
    app.run(host="0.0.0.0", port=10000)
