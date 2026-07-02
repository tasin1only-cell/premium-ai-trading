import numpy as np
import time

last_candle = -1
last_signal = "WAIT"
signal_memory = []   # 🧠 short memory


# ================= EMA =================
def ema(data, period):
    if len(data) < period:
        return data[-1] if data else 0

    alpha = 2 / (period + 1)
    result = np.mean(data[:period])

    for p in data[period:]:
        result = alpha * p + (1 - alpha) * result

    return result


# ================= RSI =================
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


# ================= MACD =================
def macd(data):
    if len(data) < 26:
        return 0
    return ema(data, 12) - ema(data, 26)


# ================= VOLATILITY =================
def volatility(data, n=10):
    if len(data) < n:
        return 0

    window = data[-n:]
    return np.std(window)


# ================= LEVEL 8C ENGINE =================
def ai_engine(prices, candle_start):

    global last_candle, last_signal, signal_memory

    if len(prices) < 40:
        return {
            "signal": "WAIT",
            "confidence": 50,
            "trend": "SIDE",
            "market": "WARMUP",
            "risk": "LOW",
            "strength": "NONE",
            "price": prices[-1] if prices else 0,
            "rsi": 50,
            "probability": 0,
            "timestamp": int(time.time())
        }

    ema20 = ema(prices, 20)
    ema50 = ema(prices, 50)
    r = rsi(prices)
    m = macd(prices)

    vol = volatility(prices, 10)

    momentum = prices[-1] - prices[-5]

    score = 0

    # ================= TREND =================
    score += 30 if ema20 > ema50 else -30

    # ================= RSI FILTER =================
    if r > 62:
        score += 15
    elif r < 38:
        score -= 15

    # ================= MACD =================
    score += 20 if m > 0 else -20

    # ================= MOMENTUM =================
    if momentum > 0.4:
        score += 15
    elif momentum < -0.4:
        score -= 15

    # ================= VOLATILITY FILTER (8C KEY) =================
    if vol > 3.5:
        score *= 0.6   # reduce fake spikes impact

    # ================= SIDEWAYS DETECTION =================
    flat_market = abs(ema20 - ema50) < 0.5 and vol < 2.0

    if flat_market:
        return {
            "signal": "WAIT",
            "confidence": 60,
            "trend": "SIDE",
            "market": "CHOP_ZONE",
            "risk": "LOW",
            "strength": "NONE",
            "price": round(prices[-1], 2),
            "rsi": round(r, 2),
            "probability": 0,
            "timestamp": int(time.time())
        }

    # ================= FINAL SCORE =================
    probability = max(5, min(95, 50 + score))

    if score >= 38:
        signal = "BUY"
        trend = "UP"
    elif score <= -38:
        signal = "SELL"
        trend = "DOWN"
    else:
        signal = "WAIT"
        trend = "SIDE"

    # ================= SIGNAL MEMORY (ANTI SPAM) =================
    signal_memory.append(signal)
    if len(signal_memory) > 5:
        signal_memory.pop(0)

    # if last 3 same → force WAIT (avoid fake trend lock)
    if signal_memory.count(signal) >= 4:
        signal = "WAIT"
        trend = "SIDE"

    # ================= CANDLE CONTROL =================
    if candle_start != last_candle:
        last_candle = candle_start
        last_signal = signal
    else:
        signal = last_signal

    confidence = min(92, 55 + abs(score))

    return {
        "signal": signal,
        "confidence": round(confidence, 2),
        "probability": round(probability, 2),
        "trend": trend,
        "market": "LIVE",
        "risk": "MEDIUM",
        "strength": "STRONG" if abs(score) > 50 else "MEDIUM",

        "price": round(prices[-1], 2),
        "rsi": round(r, 2),
        "ema20": round(ema20, 2),
        "ema50": round(ema50, 2),
        "macd": round(m, 4),
        "volatility": round(vol, 3),

        "timestamp": int(time.time())
    }
