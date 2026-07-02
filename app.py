from flask import Flask, jsonify, render_template
from flask_cors import CORS
import threading
import time
import requests
from ai_engine import ai_engine

app = Flask(__name__)
CORS(app)

prices = []
candle_start = int(time.time())

SYMBOL = "BTCUSDT"

def get_binance_price():
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={SYMBOL}"
        data = requests.get(url, timeout=3).json()
        return float(data["price"])
    except:
        return None


def price_loop():
    global candle_start

    while True:
        price = get_binance_price()

        if price:
            prices.append(price)

        if len(prices) > 2000:
            prices.pop(0)

        # candle reset (stable)
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
        "running": True
    })


@app.route("/api/history")
def history():
    return jsonify(prices[-100:])


threading.Thread(target=price_loop, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
