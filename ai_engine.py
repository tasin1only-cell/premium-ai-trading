import numpy as np
import time

# ======================
# GLOBAL CANDLE LOCK
# ======================
last_signal_minute = -1


# ======================
# EMA
# ======================
def ema(data, period):
    if len(data) < period:
        return np.mean(data) if data else 0

    alpha = 2 / (period + 1)
    result = np.mean(data[:period])

    for price in data[period:]:
        result = alpha * price + (1 - alpha) * result

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

    ema12 = ema(data, 12)
    ema26 = ema(data, 26)

    return ema12 - ema26


# ======================
# MARKET STATE
# ======================
def market_state(ema20, ema50, momentum, rsi_val):
    if abs(ema20 - ema50) < 0.25 and 45 < rsi_val < 55:
        return "SIDEWAYS"

    if momentum > 1:
        return "TRENDING_UP"

    if momentum < -1:
        return "TRENDING_DOWN"

    return "NORMAL"


# ======================
# RISK ENGINE
# ======================
def risk_score(rsi_val, macd_val):
    risk = 0

    if rsi_val > 70 or rsi_val < 30:
        risk += 2

    if abs(macd_val) > 0.5:
        risk += 2

    if risk == 0:
        return "LOW"
    elif risk == 2:
        return "MEDIUM"
    else:
        return "HIGH"


# ======================
# MAIN AI ENGINE (LEVEL 8 STABLE)
# ======================
def ai_engine(prices):

    global last_signal_minute

    if len(prices) < 50:
        return {
            "signal": "WAIT",
            "confidence": 50,
            "probability": 0,
            "trend": "SIDE",
            "market": "UNKNOWN",
            "risk": "UNKNOWN",
            "strength": "NONE",
            "price": round(prices[-1], 2) if prices else 0,
            "rsi": 50,
            "ema20": 0,
            "ema50": 0,
            "macd": 0
        }

    now = time.time()
    current_minute = int(now // 60)

    # ======================
    # INDICATORS
    # ======================
    ema20 = ema(prices, 20)
    ema50 = ema(prices, 50)
    current_rsi = rsi(prices)
    current_macd = macd(prices)

    # SAFE MOMENTUM
    momentum = prices[-1] - prices[-20] if len(prices) >= 20 else 0

    # ======================
    # SAME CANDLE LOCK
    # ======================
    if current_minute == last_signal_minute:
        return {
            "signal": "WAIT",
            "confidence": 50,
            "probability": 0,
            "trend": "SIDE",
            "market": "HOLD",
            "risk": "LOW",
            "strength": "NONE",
            "price": round(prices[-1], 2),
            "rsi": round(current_rsi, 2),
            "ema20": round(ema20, 2),
            "ema50": round(ema50, 2),
            "macd": round(current_macd, 4)
        }

    # ======================
    # ANALYSIS
    # ======================
    market = market_state(ema20, ema50, momentum, current_rsi)
    risk = risk_score(current_rsi, current_macd)

    score = 0

    if ema20 > ema50:
        score += 35
    else:
        score -= 35

    if current_rsi < 45:
        score += 25
    elif current_rsi > 55:
        score -= 25

    if current_macd > 0:
        score += 25
    elif current_macd < 0:
        score -= 25

    if momentum > 0.5:
        score += 15
    elif momentum < -0.5:
        score -= 15

    # ======================
    # PROBABILITY ENGINE
    # ======================
    probability = max(1, min(99, 50 + score))
    strength = (
        "STRONG" if abs(score) > 60 else
        "MEDIUM" if abs(score) > 30 else
        "WEAK"
    )

    base_conf = 55 + abs(score)

    # ======================
    # DECISION
    # ======================
    if score >= 60:
        signal = "BUY"
        trend = "UP"
        confidence = min(95, base_conf + 10)
        last_signal_minute = current_minute

    elif score <= -60:
        signal = "SELL"
        trend = "DOWN"
        confidence = min(95, base_conf + 10)
        last_signal_minute = current_minute

    else:
        signal = "WAIT"
        trend = "SIDE"
        confidence = 50

    return {
        "signal": signal,
        "confidence": round(confidence, 2),
        "probability": round(probability, 2),
        "trend": trend,
        "market": market,
        "risk": risk,
        "strength": strength,
        "price": round(prices[-1], 2),
        "rsi": round(current_rsi, 2),
        "ema20": round(ema20, 2),
        "ema50": round(ema50, 2),
        "macd": round(current_macd, 4)
    }
