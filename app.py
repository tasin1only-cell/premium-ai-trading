from flask import Flask, jsonify, render_template
from flask_cors import CORS
import time

from ai_engine import ai_engine
from market_feed import prices
from analytics import calculate_winrate

app = Flask(__name__)
CORS(app)

# ==========================
# CANDLE CONTROL
# ==========================
candle_start = int(time.time())


# ==========================
# HOME
# ==========================
@app.route("/")
def home():
    return render_template("index.html")


# ==========================
# SIGNAL API (MAIN)
# ==========================
@app.route("/api/signal")
def signal():

    global candle_start

    # reset candle every 60 sec
    if int(time.time()) - candle_start >= 60:
        candle_start = int(time.time())

    return jsonify(
        ai_engine(prices, candle_start)
    )


# ==========================
# STATUS API
# ==========================
@app.route("/api/status")
def status():

    return jsonify({
        "running": True,
        "market": "LEVEL 9 AI ENGINE",
        "price_len": len(prices),
        "last_price": prices[-1] if prices else 0,
        "candle_start": candle_start
    })


# ==========================
# ANALYTICS API (NEW LEVEL 9)
# ==========================
@app.route("/api/analytics")
def analytics():

    return jsonify(
        calculate_winrate()
    )


# ==========================
# PRICE HISTORY
# ==========================
@app.route("/api/history")
def history():

    return jsonify(
        prices[-100:]
    )


# ==========================
# RUN SERVER
# ==========================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=10000
    )
