from flask import Flask, jsonify, render_template
from flask_cors import CORS
import time
import threading
import random

from ai_engine import ai_engine
from market_feed import prices

app = Flask(__name__)
CORS(app)

candle_start = int(time.time())


# ==========================
# SAFETY: ENSURE PRICE EXISTS
# ==========================
def safe_last_price():
    return prices[-1] if prices else 100000.0


# ==========================
# HOME
# ==========================
@app.route("/")
def home():
    return render_template("index.html")


# ==========================
# SIGNAL API (LEVEL 8B)
# ==========================
@app.route("/api/signal")
def signal():

    global candle_start

    now = int(time.time())

    # candle reset (1 minute)
    if now - candle_start >= 60:
        candle_start = now

    return jsonify(
        ai_engine(
            prices,
            candle_start
        )
    )


# ==========================
# STATUS API (FIXED)
# ==========================
@app.route("/api/status")
def status():

    return jsonify({

        "running": True,

        "market": "BINANCE LIVE",

        "price_len": len(prices),

        "last_price": safe_last_price(),

        "candle_start": candle_start,

        "feed_alive": len(prices) > 0,

        "level": "8B HYBRID AI"

    })


# ==========================
# HISTORY API
# ==========================
@app.route("/api/history")
def history():

    return jsonify(
        prices[-100:]
    )


# ==========================
# OPTIONAL DEBUG FEED
# ==========================
@app.route("/api/feed")
def feed():

    return jsonify({

        "count": len(prices),

        "last": safe_last_price(),

        "status": "STREAMING"
    })


# ==========================
# START SERVER
# ==========================
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=10000,
        debug=False,
        threaded=True
        )
