from flask import Flask, jsonify, render_template
from flask_cors import CORS
import time

from ai_engine import ai_engine
from market_feed import prices

app = Flask(__name__)
CORS(app)

candle_start = int(time.time())


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/signal")
def signal():

    global candle_start

    if int(time.time()) - candle_start >= 60:
        candle_start = int(time.time())

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

        "market": "BINANCE LIVE",

        "price_len": len(prices),

        "last_price":

            prices[-1]

            if prices

            else 0,

        "candle_start":

            candle_start

    })


@app.route("/api/history")
def history():

    return jsonify(

        prices[-100:]

    )


if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=10000

    )
