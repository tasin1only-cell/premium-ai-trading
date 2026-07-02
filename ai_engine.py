import numpy as np
import time
from ml_model import load_model, predict

model = load_model()

last_signal = "WAIT"


def ema(data, period):
    if len(data) < period:
        return data[-1]
    alpha = 2/(period+1)
    res = np.mean(data[:period])
    for p in data[period:]:
        res = alpha*p + (1-alpha)*res
    return res


def rsi(data, period=14):
    if len(data) < period+1:
        return 50

    gains, losses = [], []

    for i in range(1, period+1):
        diff = data[-i] - data[-i-1]
        if diff > 0:
            gains.append(diff)
        else:
            losses.append(abs(diff))

    ag = np.mean(gains) if gains else 0.01
    al = np.mean(losses) if losses else 0.01

    rs = ag/al
    return 100 - (100/(1+rs))


def macd(data):
    if len(data) < 26:
        return 0
    return ema(data,12) - ema(data,26)


def features(prices):
    price = prices[-1]
    ema20 = ema(prices,20)
    ema50 = ema(prices,50)
    r = rsi(prices)
    m = macd(prices)
    momentum = prices[-1] - prices[-5]

    return [price, ema20, ema50, r, m, momentum]


def ai_engine(prices, candle_start):

    global last_signal

    if len(prices) < 60:
        return {
            "signal":"WAIT",
            "confidence":50,
            "trend":"SIDE",
            "market":"WARMUP",
            "risk":"LOW",
            "strength":"NONE",
            "price":prices[-1] if prices else 0,
            "rsi":50,
            "probability":0,
            "timestamp":int(time.time())
        }

    X = features(prices)

    if model:
        pred, prob = predict(model, X)

        if pred == 0:
            signal = "BUY"
            trend = "UP"
        elif pred == 1:
            signal = "SELL"
            trend = "DOWN"
        else:
            signal = "WAIT"
            trend = "SIDE"

        confidence = prob * 100

    else:
        signal = "WAIT"
        trend = "SIDE"
        confidence = 50

    # anti spam stability
    if signal == last_signal and confidence < 70:
        signal = "WAIT"

    last_signal = signal

    return {
        "signal": signal,
        "confidence": round(confidence,2),
        "trend": trend,
        "market": "ML-LIVE",
        "risk": "MEDIUM",
        "strength": "STRONG" if confidence > 80 else "MEDIUM",

        "price": round(prices[-1],2),
        "rsi": round(rsi(prices),2),
        "ema20": round(ema(prices,20),2),
        "ema50": round(ema(prices,50),2),
        "macd": round(macd(prices),4),

        "timestamp": int(time.time())
    }
