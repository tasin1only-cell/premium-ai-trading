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
# PRICE FEED (STABLE)
# ======================
def price_loop():
    price = 100

    while True:
        price += random.uniform(-1.2, 1.2)
        prices.append(round(price, 2))

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
        "count": len(prices),
        "last": prices[-5:] if prices else []
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
