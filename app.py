from flask import Flask, jsonify, render_template
from flask_cors import CORS
import threading
import time
from ai_engine import ai_engine

app = Flask(__name__)
CORS(app)

prices = []
candle_start = int(time.time())

# ===============================
# TEST PRICE FEED
# ===============================
def get_binance_price():
    return 100000.0


# ===============================
# STABLE LOOP
# ===============================
def price_loop():
    global candle_start

    last_price = 100000.0

    while True:

        price = get_binance_price()

        if price is None:
            price = last_price

        if price > 0:
            prices.append(price)
            last_price = price

        if len(prices) > 2000:
            prices.pop(0)

        # 1 minute candle
        if int(time.time()) - candle_start >= 60:
            candle_start = int(time.time())

        time.sleep(1)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/signal")
def signal():
    return jsonify(ai_engine(prices, candle_start))


@app.route("/api/status")
def status():
    return jsonify({
        "candle_start": candle_start,
        "price_len": len(prices),
        "running": True,
        "last_price": prices[-1] if prices else 0
    })


@app.route("/api/history")
def history():
    return jsonify(prices[-100:])


threading.Thread(
    target=price_loop,
    daemon=True
).start()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=10000
    )
