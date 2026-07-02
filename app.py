from flask import Flask, jsonify, render_template
from flask_cors import CORS
import threading
import time
import random
from ai_engine import ai_engine

app = Flask(__name__)
CORS(app)

prices = []

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


@app.route("/api/signal")
def signal():
    try:
        return jsonify(ai_engine(prices))
    except:
        return jsonify({
            "signal": "WAIT",
            "confidence": 50,
            "probability": 0,
            "trend": "SIDE",
            "market": "SAFE_MODE",
            "risk": "LOW",
            "strength": "NONE",
            "price": prices[-1] if prices else 0,
            "rsi": 50,
            "ema20": 0,
            "ema50": 0,
            "macd": 0,
            "timestamp": int(time.time())
        })


@app.route("/api/debug")
def debug():
    return {
        "price_count": len(prices),
        "last_price": prices[-1] if prices else 0,
        "status": "running"
    }


threading.Thread(target=price_loop, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
