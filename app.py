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


# TEST FEED
def get_binance_price():

    base = 100000

    move = random.uniform(-30, 30)

    return round(base + move, 2)


def price_loop():

    global candle_start

    last_price = 100000

    while True:

        price = get_binance_price()

        if price is None:
            price = last_price

        if len(prices) == 0:

            prices.extend([price] * 60)

        else:

            prices.append(price)

        last_price = price

        if len(prices) > 2000:
            prices.pop(0)

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

        "running": True,

        "price_len": len(prices),

        "last_price": prices[-1] if prices else 0,

        "candle_start": candle_start

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
