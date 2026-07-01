import numpy as np
import time

# ======================
# GLOBAL LOCK
# ======================
last_signal_time = 0


# ======================
# EMA (FIXED + STABLE)
# ======================
def ema(data, period):
    if len(data) < period:
        return np.mean(data) if data else 0

    alpha = 2 / (period + 1)

    result = np.mean(data[:period])  # 🔥 stable seed

    for price in data[period:]:
        result = alpha * price + (1 - alpha) * result

    return result


# ======================
# RSI (STABLE)
# ======================
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


# ======================
# MACD (REAL STRUCTURE FIX)
# ======================
def macd(data):
    if len(data) < 30:
        return 0

    ema12 = ema(data[-100:], 12)
    ema26 = ema(data[-100:], 26)

    return ema12 - ema26


# ======================
# AI ENGINE (LEVEL 7 READY)
# ======================
def ai_engine(prices):
    global last_signal_time

    if len(prices) < 50:
        return {
            "signal": "WAIT",
            "confidence": 50,
            "trend": "SIDE",
            "price": prices[-1] if prices else 0,
            "rsi": 50,
            "ema20": 0,
            "ema50": 0,
            "macd": 0
        }

    now = time.time()

    # 🔥 60 sec candle lock
    if now - last_signal_time < 60:
        return {
            "signal": "WAIT",
            "confidence": 50,
            "trend": "SIDE",
            "price": round(prices[-1], 2),
            "rsi": 50,
            "ema20": 0,
            "ema50": 0,
            "macd": 0
        }

    # ======================
    # INDICATORS
    # ======================
    ema20 = ema(prices, 20)
    ema50 = ema(prices, 50)
    current_rsi = rsi(prices)
    current_macd = macd(prices)

    score = 0

    # ======================
    # TREND FILTER
    # ======================
    if ema20 > ema50:
        score += 30
    else:
        score -= 30

    # ======================
    # RSI FILTER
    # ======================
    if current_rsi < 45:
        score += 25
    elif current_rsi > 55:
        score -= 25

    # ======================
    # MACD FILTER
    # ======================
    if current_macd > 0.02:
        score += 25
    elif current_macd < -0.02:
        score -= 25

    # ======================
    # MOMENTUM
    # ======================
    momentum = prices[-1] - prices[-20]

    if momentum > 0.5:
        score += 20
    elif momentum < -0.5:
        score -= 20

    # ======================
    # FINAL DECISION
    # ======================
    base_conf = 55 + abs(score)

    if score >= 60:
        signal = "BUY"
        trend = "UP"
        confidence = min(95, base_conf + 8)

    elif score <= -60:
        signal = "SELL"
        trend = "DOWN"
        confidence = min(95, base_conf + 8)

    else:
        signal = "WAIT"
        trend = "SIDE"
        confidence = 50

    last_signal_time = now

    return {
        "signal": signal,
        "confidence": round(confidence, 2),
        "trend": trend,
        "price": round(prices[-1], 2),
        "rsi": round(current_rsi, 2),
        "ema20": round(ema20, 2),
        "ema50": round(ema50, 2),
        "macd": round(current_macd, 4)
    }
