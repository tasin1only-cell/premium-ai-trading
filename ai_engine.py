import numpy as np
import time

last_candle = -1

def ema(data, p):
    if len(data) < p:
        return data[-1] if data else 0

    alpha = 2 / (p + 1)
    e = np.mean(data[:p])

    for x in data[p:]:
        e = alpha * x + (1 - alpha) * e

    return e


def rsi(data, p=14):
    if len(data) < p + 1:
        return 50

    gains, losses = [], []

    for i in range(1, p + 1):
        diff = data[-i] - data[-i - 1]
        if diff > 0:
            gains.append(diff)
        else:
            losses.append(abs(diff))

    ag = np.mean(gains) if gains else 0.01
    al = np.mean(losses) if losses else 0.01

    rs = ag / al
    return 100 - (100 / (1 + rs))


def macd(data):
    if len(data) < 30:
        return 0

    return ema(data, 12) - ema(data, 26)


def ai_engine(prices):

    global last_candle

    if len(prices) < 30:
        return {
            "signal": "WAIT",
            "confidence": 50,
            "probability": 0,
            "trend": "SIDE",
            "market": "WARMUP",
            "risk": "LOW",
            "strength": "NONE",
            "price": prices[-1] if prices else 0,
            "rsi": 50,
            "ema20": 0,
            "ema50": 0,
            "macd": 0
        }

    ema20 = ema(prices, 20)
    ema50 = ema(prices, 50)
    r = rsi(prices)
    m = macd(prices)
    momentum = prices[-1] - prices[-10]

    score = 0

    if ema20 > ema50:
        score += 30
    else:
        score -= 30

    if r < 45:
        score += 20
    elif r > 55:
        score -= 20

    if m > 0:
        score += 20
    else:
        score -= 20

    if momentum > 0.3:
        score += 15
    elif momentum < -0.3:
        score -= 15

    probability = min(99, max(1, 50 + score))

    if score >= 50:
        signal = "BUY"
        trend = "UP"
    elif score <= -50:
        signal = "SELL"
        trend = "DOWN"
    else:
        signal = "WAIT"
        trend = "SIDE"

    return {
        "signal": signal,
        "confidence": min(95, 55 + abs(score)),
        "probability": probability,
        "trend": trend,
        "market": "ACTIVE",
        "risk": "MEDIUM",
        "strength": "STRONG" if abs(score) > 50 else "MEDIUM",
        "price": round(prices[-1], 2),
        "rsi": round(r, 2),
        "ema20": round(ema20, 2),
        "ema50": round(ema50, 2),
        "macd": round(m, 4)
    }
