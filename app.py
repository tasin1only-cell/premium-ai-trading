from flask import Flask, jsonify, render_template
from flask_cors import CORS
import threading
import time
import random
from ai_engine import ai_engine

app = Flask(__name__)
CORS(app)

prices = []

# 🔥 CANDLE STATE
current_candle = int(time.time() // 60)

def price_loop():
    price = 100
    global current_candle

    while True:
        price += random.uniform(-1.2, 1.2)
        prices.append(price)

        if len(prices) > 2000:
            prices.pop(0)

        # candle update
        current_candle = int(time.time() // 60)

        time.sleep(1)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/signal")
def signal():
    return jsonify(ai_engine(prices, current_candle))


@app.route("/api/history")
def history():
    return jsonify(prices[-100:])


@app.route("/api/status")
def status():
    return jsonify({
        "candle_start": current_candle
    })


threading.Thread(target=price_loop, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
