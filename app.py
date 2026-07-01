from flask import Flask, jsonify
from flask_cors import CORS
import random
import numpy as np

app = Flask(__name__)
CORS(app)

# ======================
# MARKET DATA
# ======================
prices = [100 + random.uniform(-1, 1) for _ in range(300)]


# ======================
# UPDATE PRICE
# ======================
def update_price():
    global prices
    change = random.uniform(-1.2, 1.2)
    prices.append(prices[-1] + change)

    if len(prices) > 500:
        prices.pop(0)


# ======================
# SIMPLE AI FEATURES
# ======================
def get_features(data):
    window = data[-20:]

    momentum = window[-1] - window[0]
    volatility = np.std(window)
    mean_price = np.mean(window)

    return momentum, volatility, mean_price


# ======================
# SIMPLE AI ENGINE (STABLE)
# ======================
def ai_engine(data):

    momentum, volatility, mean_price = get_features(data)
    price = data[-1]

    # base probabilities
    buy = 0.5
    sell = 0.5

    # momentum effect
    if momentum > 0:
        buy += 0.2
    else:
        sell += 0.2

    # volatility control
    if volatility > 2:
        buy -= 0.05
        sell -= 0.05

    # price relation
    if price > mean_price:
        buy += 0.1
    else:
        sell += 0.1

    total = buy + sell

    buy_prob = buy / total
    sell_prob = sell / total

    if buy_prob > 0.6:
        signal = "BUY"
    elif sell_prob > 0.6:
        signal = "SELL"
    else:
        signal = "WAIT"

    confidence = max(buy_prob, sell_prob) * 100

    return {
        "price": round(price, 2),
        "signal": signal,
        "confidence": round(confidence, 2),
        "buy_probability": round(buy_prob, 2),
        "sell_probability": round(sell_prob, 2),
    }


# ======================
# ROUTES
# ======================
@app.route("/")
def home():
    return "AI Trading Pro Running ✔"


@app.route("/api/signal")
def signal():
    update_price()
    return jsonify(ai_engine(prices))


@app.route("/api/history")
def history():
    return jsonify(prices)


# ======================
# IMPORTANT RENDER FIX
# ======================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
