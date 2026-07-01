from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
import eventlet
import numpy as np
from binance import ThreadedWebsocketManager

eventlet.monkey_patch()

app = Flask(__name__)
CORS(app)

socketio = SocketIO(app, cors_allowed_origins="*")

# ======================
# LIVE PRICES
# ======================
prices = []


# ======================
# AI ENGINE
# ======================
def ai_engine(data):

    window = data[-30:]

    momentum = window[-1] - window[0]
    volatility = np.std(window)
    mean_price = np.mean(window)

    buy = 50
    sell = 50

    buy += momentum * 2
    sell -= momentum * 2

    if volatility > 2:
        buy -= 5
        sell -= 5

    if window[-1] > mean_price:
        buy += 10
    else:
        sell += 10

    total = buy + sell
    buy_prob = buy / total
    sell_prob = sell / total

    if buy_prob > 0.6:
        signal = "BUY"
    elif sell_prob > 0.6:
        signal = "SELL"
    else:
        signal = "WAIT"

    rsi = 50 + (buy_prob - sell_prob) * 50

    return {
        "price": round(window[-1], 2),
        "signal": signal,
        "buy": round(buy_prob, 2),
        "sell": round(sell_prob, 2),
        "rsi": round(rsi, 2)
    }


# ======================
# EMIT REALTIME SIGNAL
# ======================
def emit_signal():
    if len(prices) < 30:
        return

    data = ai_engine(prices)

    socketio.emit("update", {
        "price": data["price"],
        "signal": data["signal"],
        "rsi": data["rsi"],
        "confidence": round(data["buy"] * 100, 2),
        "trend": "UP" if data["signal"] == "BUY" else "DOWN"
    })


# ======================
# BINANCE STREAM
# ======================
def handle_message(msg):
    global prices

    price = float(msg['c'])
    prices.append(price)

    if len(prices) > 500:
        prices.pop(0)

    if len(prices) > 30:
        emit_signal()


def start_stream():
    twm = ThreadedWebsocketManager()
    twm.start()

    twm.start_symbol_ticker_socket(
        callback=handle_message,
        symbol="BTCUSDT"
    )


# ======================
# ROUTES
# ======================
@app.route("/")
def home():
    return "AI Trading Pro Running ✔"


# ✅ FIXED API ROUTE (THIS WAS MISSING BEFORE)
@app.route("/api/signal")
def signal():

    if len(prices) < 30:
        return jsonify({
            "signal": "WAIT",
            "price": 0,
            "confidence": 0,
            "trend": "SIDE",
            "rsi": 50
        })

    data = ai_engine(prices)

    return jsonify({
        "price": data["price"],
        "signal": data["signal"],
        "confidence": round(data["buy"] * 100, 2),
        "trend": "UP" if data["signal"] == "BUY" else "DOWN",
        "rsi": data["rsi"]
    })


@app.route("/api/history")
def history():
    return jsonify(prices[-100:])


# ======================
# SOCKET
# ======================
@socketio.on("connect")
def connect():
    print("Client Connected ✔")


# ======================
# RUN
# ======================
if __name__ == "__main__":
    socketio.start_background_task(start_stream)
    socketio.run(app, host="0.0.0.0", port=10000)
