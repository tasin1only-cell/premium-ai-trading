from flask import Flask, jsonify
from flask_cors import CORS
import random
import numpy as np
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)
CORS(app)

# ======================
# SIMULATED MARKET DATA
# ======================
prices = [100 + random.uniform(-1, 1) for _ in range(300)]


# ======================
# FEATURE ENGINE
# ======================
def make_features(data):
    X = []

    for i in range(20, len(data)):
        window = data[i-20:i]

        rsi = sum(max(0, window[j]-window[j-1]) for j in range(1,20))
        ema = np.mean(window)
        momentum = window[-1] - window[0]
        volatility = np.std(window)

        X.append([rsi, ema, momentum, volatility])

    return np.array(X)


# ======================
# LABEL GENERATION (TRAINING DATA)
# ======================
def make_labels(data):
    y = []

    for i in range(20, len(data)):
        if data[i] > data[i-1]:
            y.append(1)   # BUY
        else:
            y.append(0)   # SELL

    return np.array(y)


# ======================
# TRAIN MODEL
# ======================
def train_model(data):
    X = make_features(data)
    y = make_labels(data)

    model = RandomForestClassifier(n_estimators=50)
    model.fit(X, y)

    return model


# ======================
# UPDATE PRICE
# ======================
def update_price():
    global prices
    change = random.uniform(-1.5, 1.5)
    prices.append(prices[-1] + change)

    if len(prices) > 400:
        prices.pop(0)


# ======================
# GET CURRENT FEATURE
# ======================
def current_feature(data):
    window = data[-20:]

    rsi = sum(max(0, window[i]-window[i-1]) for i in range(1,20))
    ema = np.mean(window)
    momentum = window[-1] - window[0]
    volatility = np.std(window)

    return np.array([[rsi, ema, momentum, volatility]])


# ======================
# ROUTE
# ======================
@app.route("/api/signal")
def signal():

    update_price()

    model = train_model(prices)

    X = current_feature(prices)

    prediction = model.predict(X)[0]
    prob = model.predict_proba(X)[0]

    signal = "BUY" if prediction == 1 else "SELL"
    confidence = float(max(prob)) * 100

    return jsonify({
        "price": round(prices[-1], 2),
        "signal": signal,
        "confidence": round(confidence, 2),
        "buy_prob": round(prob[1], 2),
        "sell_prob": round(prob[0], 2)
    })


@app.route("/api/history")
def history():
    return jsonify(prices)


# ======================
# RUN
# ======================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)