import numpy as np
import time

last_candle = -1


def ema(data, period):
    if len(data) < period:
        return data[-1] if data else 0

    alpha = 2 / (period + 1)
    result = np.mean(data[:period])

    for p in data[period:]:
        result = alpha * p + (1 - alpha) * result

    return result


def rsi(data, period=14):
    if len(data) < period + 1:
        return 50

    gains, losses = [], []

    for i in range(1, period + 1):
        diff = data[-i] - data[-i - 1]
        if diff > 0:
            gains.append(diff)
        else:
            losses.append(abs(diff))

    avg_gain = np.mean(gains) if gains else 0.01
    avg_loss = np.mean(losses) if losses else 0.01

    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def macd(data):
    if len(data) < 30:
        return 0
    return ema(data, 12) - ema(data, 26)


# 🔥 SAFE ENGINE
def ai_engine(prices, candle_start):
    global last_candle

    # ❌ safety: no data
    if not prices or len(prices) < 50 or prices[-1] == 0:
        return {
            "signal": "WAIT",
            "confidence": 50,
            "trend": "SIDE",
            "market": "NO_DATA",
            "risk": "LOW",
            "strength": "NONE",
            "price": prices[-1] if prices else 0,
            "rsi": 50,
            "probability": 0,
            "timestamp": int(time.time())
        }

    # candle lock protection
    if candle_start == last_candle:
        return {
            "signal": "WAIT",
            "confidence": 50,
            "trend": "SIDE",
            "market": "SYNCED",
            "risk": "LOW",
            "strength": "NONE",
            "price": prices[-1],
            "rsi": rsi(prices),
            "probability": 0,
            "timestamp": int(time.time())
        }

    ema20 = ema(prices, 20)
    ema50 = ema(prices, 50)
    r = rsi(prices)
    m = macd(prices)

    # safer momentum
    momentum = prices[-1] - prices[-10] if len(prices) > 10 else 0

    score = 0

    # TREND
    score += 40 if ema20 > ema50 else -40

    # RSI FILTER
    if r < 40:
        score += 25
    elif r > 60:
        score -= 25

    # MACD
    score += 20 if m > 0 else -20

    # MOMENTUM
    if momentum > 0.8:
        score += 15
    elif momentum < -0.8:
        score -= 15

    probability = min(99, max(1, 50 + score))

    if score >= 60:
        signal = "BUY"
        trend = "UP"
    elif score <= -60:
        signal = "SELL"
        trend = "DOWN"
    else:
        signal = "WAIT"
        trend = "SIDE"

    last_candle = candle_start

    return {
        "signal": signal,
        "confidence": min(95, 55 + abs(score)),
        "probability": probability,
        "trend": trend,
        "market": "LIVE",
        "risk": "MEDIUM",
        "strength": "STRONG" if abs(score) > 60 else "MEDIUM",
        "price": round(prices[-1], 2),
        "rsi": round(r, 2),
        "ema20": round(ema20, 2),
        "ema50": round(ema50, 2),
        "macd": round(m, 4),
        "timestamp": int(time.time())
    }
