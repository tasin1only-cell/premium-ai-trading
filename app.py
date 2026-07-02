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
# IMPROVED TEST FEED (SMOOTH TREND)
# ==========================
def get_binance_price():

    global current_price

    # smoother movement (LESS RANDOM SPIKE)
    move = random.uniform(-2.5, 2.5)

    current_price += move

    return round(current_price, 2)


# ==========================
# PRICE LOOP (STABLE + SEED FIX)
# ==========================
def price_loop():

    global candle_start

    while True:

        price = get_binance_price()

        if not prices:

            # better seed (avoid RSI 100 / flat EMA)
            temp = price

            seed = []

            for _ in range(60):

                temp += random.uniform(-2, 2)

                seed.append(round(temp, 2))

            prices.extend(seed)

        else:

            prices.append(price)

        # limit memory
        if len(prices) > 2000:

            prices.pop(0)

        # candle sync (1 min)
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

    return jsonify(

        ai_engine(

            prices,

            candle_start

        )

    )


@app.route("/api/status")
def status():

    return jsonify({

        "running": True,

        "price_len": len(prices),

        "last_price":

            prices[-1]

            if prices

            else 0,

        "candle_start": candle_start

    })


@app.route("/api/history")
def history():

    return jsonify(

        prices[-100:]

    )


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
