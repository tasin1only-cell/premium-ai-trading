import numpy as np

last_candle = -1

# ======================
# EMA
# ======================
def ema(data, period):
    if len(data) < period:
        return data[-1] if data else 0

    alpha = 2 / (period + 1)
    result = np.mean(data[:period])

    for p in data[period:]:
        result = alpha * p + (1 - alpha) * result

    return result


# ======================
# RSI
# ======================
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


# ======================
# MACD
# ======================
def macd(data):
    if len(data) < 30:
        return 0

    return ema(data, 12) - ema(data, 26)


# ======================
# ENGINE (LEVEL 9)
# ======================
def ai_engine(prices, candle_id):

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

    # 🔥 LOCK SAME CANDLE
    if candle_id == last_candle:
        return {
            "signal": "WAIT",
            "confidence": 50,
            "probability": 0,
            "trend": "SIDE",
            "market": "HOLD",
            "risk": "LOW",
            "strength": "NONE",
            "price": prices[-1],
            "rsi": rsi(prices),
            "ema20": ema(prices, 20),
            "ema50": ema(prices, 50),
            "macd": macd(prices)
        }

    ema20 = ema(prices, 20)
    ema50 = ema(prices, 50)
    r = rsi(prices)
    m = macd(prices)

    momentum = prices[-1] - prices[-10]

    score = 0

    if ema20 > ema50:
        score += 35
    else:
        score -= 35

    if r < 45:
        score += 25
    elif r > 55:
        score -= 25

    if m > 0:
        score += 20
    else:
        score -= 20

    if momentum > 0.5:
        score += 20
    elif momentum < -0.5:
        score -= 20

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

    last_candle = candle_id

    return {
        "signal": signal,
        "confidence": min(95, 55 + abs(score)),
        "probability": probability,
        "trend": trend,
        "market": "ACTIVE",
        "risk": "MEDIUM",
        "strength": "STRONG" if abs(score) > 60 else "MEDIUM",
        "price": round(prices[-1], 2),
        "rsi": round(r, 2),
        "ema20": round(ema20, 2),
        "ema50": round(ema50, 2),
        "macd": round(m, 4)
    }
