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

# 🔥 SAFE PRICE FETCH
def get_binance_price():
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={SYMBOL}"
        r = requests.get(url, timeout=5)
        data = r.json()

        price = float(data.get("price", 0))

        if price <= 0:
            return None

        return price

    except Exception as e:
        print("PRICE FETCH ERROR:", e)
        return None


# 🔥 STABLE LOOP (NO FREEZE)
def price_loop():
    global candle_start

    last_price = 0

    while True:
        price = get_binance_price()

        # fallback system (IMPORTANT FIX)
        if price is None:
            price = last_price

        if price and price > 0:
            prices.append(price)
            last_price = price

        if len(prices) > 2000:
            prices.pop(0)

        # candle sync (stable)
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
