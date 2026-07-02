from flask import Flask, jsonify, render_template
from flask_cors import CORS
import threading
import time
import random
from ai_engine import ai_engine

app = Flask(__name__)
CORS(app)

prices = []
candle_start = int(time.time())

current_price = 100000.0


# ==========================
# PRICE GENERATOR (SMOOTH + REALISTIC)
# ==========================
def get_binance_price():
    global current_price

    # smooth movement (not too random)
    move = random.uniform(-3.5, 3.5)

    current_price += move

    return round(current_price, 2)


# ==========================
# PRICE LOOP (STABLE ENGINE)
# ==========================
def price_loop():
    global candle_start

    seeded = False

    while True:

        price = get_binance_price()

        # ---------- INITIAL SEED ONCE ----------
        if not seeded:
            temp = price
            seed = []

            for _ in range(60):
                temp += random.uniform(-2.5, 2.5)
                seed.append(round(temp, 2))

            prices.extend(seed)
            seeded = True

        else:
            prices.append(price)

        # ---------- MEMORY CONTROL ----------
        if len(prices) > 2000:
            prices.pop(0)

        # ---------- CANDLE SYNC ----------
        if int(time.time()) - candle_start >= 60:
            candle_start = int(time.time())

        time.sleep(1)


# ==========================
# ROUTES
# ==========================
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/signal")
def signal():
    return jsonify(ai_engine(prices, candle_start))


@app.route("/api/status")
def status():
    return jsonify({
        "running": True,
        "price_len": len(prices),
        "last_price": prices[-1] if prices else 0,
        "candle_start": candle_start
    })


@app.route("/api/history")
def history():
    return jsonify(prices[-100:])


# ==========================
# START THREAD
# ==========================
threading.Thread(
    target=price_loop,
    daemon=True
).start()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=10000
    )
