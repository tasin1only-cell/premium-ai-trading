from flask import Flask, jsonify
from flask_cors import CORS
import numpy as np
import random
import threading
import time

app = Flask(__name__)
CORS(app)

prices = []

# =====================
# Fake feed (replace with real exchange later)
# =====================
def price_loop():
    price = 100

    while True:

        move = random.uniform(-1.2,1.2)

        price += move

        prices.append(price)

        if len(prices) > 500:
            prices.pop(0)

        time.sleep(2)


# =====================
# EMA
# =====================
def ema(data, period):

    if len(data) < period:
        return np.mean(data)

    alpha = 2/(period+1)

    result = data[0]

    for p in data:

        result = alpha*p + (1-alpha)*result

    return result


# =====================
# RSI
# =====================
def rsi(data, period=14):

    if len(data) < period+1:
        return 50

    gains = []
    losses = []

    for i in range(1,period+1):

        diff = data[-i] - data[-i-1]

        if diff > 0:
            gains.append(diff)
        else:
            losses.append(abs(diff))

    avg_gain = np.mean(gains) if gains else 0.001
    avg_loss = np.mean(losses) if losses else 0.001

    rs = avg_gain/avg_loss

    return round(
        100-(100/(1+rs)),
        2
    )


# =====================
# MACD
# =====================
def macd(data):

    ema12 = ema(data,12)

    ema26 = ema(data,26)

    return round(
        ema12-ema26,
        4
    )


# =====================
# AI ENGINE
# =====================
def ai_engine():

    if len(prices) < 50:

        return {

            "signal":"WAIT",

            "confidence":50,

            "trend":"SIDE",

            "price":0,

            "rsi":50,

            "ema20":0,

            "ema50":0,

            "macd":0

        }

    ema20 = ema(prices,20)

    ema50 = ema(prices,50)

    current_rsi = rsi(prices)

    current_macd = macd(prices)

    score = 0

    if ema20 > ema50:
        score += 30

    else:
        score -= 30

    if current_rsi < 35:
        score += 20

    elif current_rsi > 70:
        score -= 20

    if current_macd > 0:
        score += 20

    else:
        score -= 20

    if score >= 40:

        signal = "BUY"

        trend = "UP"

        confidence = min(
            90,
            60+abs(score)
        )

    elif score <= -40:

        signal = "SELL"

        trend = "DOWN"

        confidence = min(
            90,
            60+abs(score)
        )

    else:

        signal = "WAIT"

        trend = "SIDE"

        confidence = 50

    return {

        "signal":signal,

        "confidence":round(confidence,2),

        "trend":trend,

        "price":round(prices[-1],2),

        "rsi":round(current_rsi,2),

        "ema20":round(ema20,2),

        "ema50":round(ema50,2),

        "macd":round(current_macd,4)

    }


@app.route("/")
def home():

    return "AI Trading Pro Level 6A Running"


@app.route("/api/signal")
def signal():

    return jsonify(

        ai_engine()

    )


@app.route("/api/history")
def history():

    return jsonify(

        prices[-100:]

    )


if __name__ == "__main__":

    threading.Thread(

        target=price_loop,

        daemon=True

    ).start()

    app.run(

        host="0.0.0.0",

        port=10000

    )
