from flask import Flask, jsonify, render_template
from flask_cors import CORS
import threading, time, random
from ai_engine import ai_engine
from dataset_builder import save_row

app = Flask(__name__)
CORS(app)

prices = []
candle_start = int(time.time())
current_price = 100000


def get_price():
    global current_price
    current_price += random.uniform(-3,3)
    return round(current_price,2)


def price_loop():
    global candle_start

    while True:
        price = get_price()
        prices.append(price)

        if len(prices) > 2000:
            prices.pop(0)

        # OPTIONAL: dataset training logging
        if len(prices) > 60:
            save_row([
                price, price, price, 50, 0, 0, 2
            ])

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
        "candle_start": candle_start,
        "mode": "LEVEL_10_ML"
    })


threading.Thread(target=price_loop, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
