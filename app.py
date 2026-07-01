from flask import Flask, jsonify
from flask_cors import CORS
import random
import numpy as np
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)
CORS(app)

# ======================
# MARKET DATA (SIMULATED)
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
# FEATURES
# ======================
def make_features(data):
    X = []

    for i in range(20, len(data)):
        window = data[i-20:i]

        momentum = window[-1] - window[0]
        volatility = np.std(window)
        mean_price = np.mean(window)

        X.append([momentum, volatility, mean_price])

    return np.array(X)


# ======================
# LABELS
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

    model = RandomForestClassifier(n_estimators=60, random_state=42)
    model.fit(X, y)

    return model


# ======================
# CURRENT FEATURE
# ======================
def current_feature(data):
    window = data[-20:]

    momentum = window[-1] - window[0]
    volatility = np.std(window)
    mean_price = np.mean(window)

    return np.array([[momentum, volatility, mean_price]])


# ======================
# MAIN API
# ======================
@app.route("/api/signal")
def signal():

    update_price()

    model = train_model(prices)

    X = current_feature(prices)

    prediction = model.predict(X)[0]
    prob = model.predict_proba(X)[0]

    signal = "BUY" if prediction == 1 else "SELL"
    confidence = round(float(max(prob)) * 100, 2)

    trend = "UP" if prices[-1] > prices[-10] else "DOWN"

    return jsonify({
        "price": round(prices[-1], 2),
        "signal": signal,
        "confidence": confidence,
        "buy_probability": round(prob[1], 2),
        "sell_probability": round(prob[0], 2),
        "trend": trend
    })


# ======================
# HISTORY API
# ======================
@app.route("/api/history")
def history():
    return jsonify(prices)


# ======================
# HEALTH CHECK
# ======================
@app.route("/")
def home():
    return "Level 3 AI Trading Engine Running ✔"


# ======================
# RUN (RENDER READY)
# ======================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
