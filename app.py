from flask import Flask, jsonify
from flask_cors import CORS
import random
import numpy as np

app = Flask(__name__)
CORS(app)

# ======================
# LIVE MARKET SIMULATION
# ======================
prices = [100 + random.uniform(-1, 1) for _ in range(200)]


# ======================
# LIVE PRICE UPDATE
# ======================
def update_price():
    global prices
    change = random.uniform(-1.5, 1.5)
    new_price = prices[-1] + change
    prices.append(new_price)

    if len(prices) > 500:
        prices.pop(0)


# ======================
# LIVE FEATURES
# ======================
def get_features(data):
    window = data[-30:]

    momentum = window[-1] - window[0]
    volatility = np.std(window)
    mean_price = np.mean(window)

    return momentum, volatility, mean_price


# ======================
# ADAPTIVE AI ENGINE (LEVEL 4)
# ======================
def ai_engine(data):

    momentum, volatility, mean_price = get_features(data)
    price = data[-1]

    buy_score = 50
    sell_score = 50

    # momentum effect
    buy_score += momentum * 2
    sell_score -= momentum * 2

    # volatility filter (avoid chaos)
    if volatility > 2.5:
        buy_score -= 5
        sell_score -= 5

    # price trend
    if price > mean_price:
        buy_score += 10
    else:
        sell_score += 10

    # normalize
    total = buy_score + sell_score
    buy_prob = buy_score / total
    sell_prob = sell_score / total

    if buy_prob > 0.60:
        signal = "BUY"
    elif sell_prob > 0.60:
        signal = "SELL"
    else:
        signal = "WAIT"

    confidence = max(buy_prob, sell_prob) * 100

    return {
        "price": round(price, 2),
        "signal": signal,
        "confidence": round(confidence, 2),
        "buy_prob": round(buy_prob, 2),
        "sell_prob": round(sell_prob, 2),
    }


# ======================
# API ROUTES
# ======================
@app.route("/")
def home():
    return "Level 4 Live AI Engine Running ✔"


@app.route("/api/signal")
def signal():
    update_price()
    return jsonify(ai_engine(prices))


@app.route("/api/live")
def live():
    update_price()
    return jsonify({
        "price": round(prices[-1], 2),
        "history": prices[-50:]  # live mini stream
    })


@app.route("/api/history")
def history():
    return jsonify(prices)


# ======================
# RUN (RENDER SAFE)
# ======================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
