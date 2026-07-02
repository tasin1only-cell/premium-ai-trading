import numpy as np
import time

last_candle = -1
last_signal = "WAIT"


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

    gains = []
    losses = []

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

    if len(data) < 26:
        return 0

    return ema(data, 12) - ema(data, 26)


# ==========================
# LEVEL 7 STABLE + ANTI STUCK ENGINE
# ==========================
def ai_engine(prices, candle_start):

    global last_candle
    global last_signal

    # ---------- NO DATA ----------
    if not prices or len(prices) < 30:

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

    # ---------- WARMUP ----------
    if len(prices) < 50:

        return {
            "signal": "WAIT",
            "confidence": 50,
            "trend": "SIDE",
            "market": "WARMUP",
            "risk": "LOW",
            "strength": "NONE",
            "price": round(prices[-1], 2),
            "rsi": 50,
            "probability": 0,
            "timestamp": int(time.time())
        }

    ema20 = ema(prices, 20)
    ema50 = ema(prices, 50)

    r = rsi(prices)
    m = macd(prices)

    momentum = prices[-1] - prices[-15] if len(prices) > 15 else 0

    score = 0

    # ==========================
    # TREND (EMA)
    # ==========================
    score += 35 if ema20 > ema50 else -35

    # ==========================
    # RSI FILTER (SMOOTH)
    # ==========================
    if r > 62:
        score += 20
    elif r < 38:
        score -= 20

    # ==========================
    # MACD
    # ==========================
    score += 22 if m > 0 else -22

    # ==========================
    # MOMENTUM (NOISE REDUCED)
    # ==========================
    if momentum > 1.0:
        score += 12
    elif momentum < -1.0:
        score -= 12

    # ==========================
    # PROBABILITY (SMOOTHED)
    # ==========================
    probability = max(5, min(95, 50 + score))

    # ==========================
    # SIGNAL GENERATION
    # ==========================
    if score >= 48:
        signal = "BUY"
        trend = "UP"

    elif score <= -48:
        signal = "SELL"
        trend = "DOWN"

    else:
        signal = "WAIT"
        trend = "SIDE"

    # ==========================
    # ANTI STUCK SIGNAL FIX
    # ==========================
    # prevent same signal spam
    if signal == last_signal and abs(score) < 55:
        signal = "WAIT"
        trend = "SIDE"

    last_signal = signal
    last_candle = candle_start

    # ==========================
    # CONFIDENCE
    # ==========================
    confidence = min(90, 55 + abs(score) * 0.7)

    return {

        "signal": signal,
        "confidence": round(confidence, 2),
        "probability": round(probability, 2),
        "trend": trend,
        "market": "LIVE",
        "risk": "MEDIUM",
        "strength": "STRONG" if abs(score) >= 60 else "MEDIUM",

        "price": round(prices[-1], 2),
        "rsi": round(r, 2),
        "ema20": round(ema20, 2),
        "ema50": round(ema50, 2),
        "macd": round(m, 4),

        "timestamp": int(time.time())
    }
