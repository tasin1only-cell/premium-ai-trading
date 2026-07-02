import numpy as np
import time

last_signal_minute = -1

# ======================
# MEMORY (LEVEL 9)
# ======================
signal_memory = []

# ======================
# EMA
# ======================
def ema(data, period):
    if len(data) < period:
        return data[-1] if len(data) else 0

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
# QUALITY SCORE
# ======================
def quality(score):
    if abs(score) > 70:
        return "A+"
    elif abs(score) > 50:
        return "A"
    elif abs(score) > 30:
        return "B"
    else:
        return "C"

# ======================
# AI ENGINE (LEVEL 9)
# ======================
def ai_engine(prices):
    global last_signal_minute, signal_memory

    if len(prices) < 30:
        return {
            "signal": "WAIT",
            "confidence": 50,
            "probability": 0,
            "trend": "SIDE",
            "market": "WARMUP",
            "risk": "LOW",
            "strength": "NONE",
            "quality": "C",
            "price": prices[-1] if prices else 0,
            "rsi": 50,
            "ema20": 0,
            "ema50": 0,
            "macd": 0
        }

    now = time.time()
    minute = int(now // 60)

    ema20 = ema(prices, 20)
    ema50 = ema(prices, 50)
    r = rsi(prices)
    m = macd(prices)
    momentum = prices[-1] - prices[-10]

    # ======================
    # SCORE SYSTEM
    # ======================
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
    elif m < 0:
        score -= 20

    if momentum > 0.5:
        score += 20
    elif momentum < -0.5:
        score -= 20

    probability = min(99, max(1, 50 + score))

    # ======================
    # SIGNAL DECISION
    # ======================
    if minute == last_signal_minute:
        signal = "WAIT"
    else:
        if score >= 60:
            signal = "BUY"
            last_signal_minute = minute
        elif score <= -60:
            signal = "SELL"
            last_signal_minute = minute
        else:
            signal = "WAIT"

    trend = "UP" if score > 0 else "DOWN" if score < 0 else "SIDE"

    conf = min(95, 55 + abs(score))
    qual = quality(score)

    # ======================
    # STORE SIGNAL (LEVEL 9 MEMORY)
    # ======================
    signal_memory.append({
        "signal": signal,
        "price": prices[-1],
        "minute": minute,
        "score": score
    })

    if len(signal_memory) > 200:
        signal_memory.pop(0)

    return {
        "signal": signal,
        "confidence": round(conf, 2),
        "probability": round(probability, 2),
        "trend": trend,
        "market": "ACTIVE",
        "risk": "MEDIUM",
        "strength": "STRONG" if abs(score) > 60 else "MEDIUM",
        "quality": qual,
        "price": round(prices[-1], 2),
        "rsi": round(r, 2),
        "ema20": round(ema20, 2),
        "ema50": round(ema50, 2),
        "macd": round(m, 4)
    }

# ======================
# LEVEL 9 EXTRA (optional API hook use)
# ======================
def get_signal_memory():
    return signal_memory[-50:]
