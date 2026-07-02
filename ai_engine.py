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


# =====================================
# LEVEL 8B HYBRID ENGINE
# =====================================
def ai_engine(prices, candle_start):

    global last_candle
    global last_signal

    if len(prices) < 50:

        return {

            "signal": "WAIT",

            "confidence": 50,

            "trend": "SIDE",

            "market": "WARMUP",

            "market_state": "WARMUP",

            "bias": "NEUTRAL",

            "volatility": "LOW",

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

    momentum = prices[-1] - prices[-5]

    vol = np.std(prices[-20:])

    score = 0

    # ======================
    # TREND
    # ======================

    if ema20 > ema50:

        score += 30

    else:

        score -= 30

    # ======================
    # RSI
    # ======================

    if r > 60:

        score += 20

    elif r < 40:

        score -= 20

    # ======================
    # MACD
    # ======================

    if m > 0:

        score += 25

    else:

        score -= 25

    # ======================
    # MOMENTUM
    # ======================

    if momentum > 0.3:

        score += 15

    elif momentum < -0.3:

        score -= 15

    # ======================
    # SIGNAL
    # ======================

    if score >= 40:

        signal = "BUY"

        trend = "UP"

    elif score <= -40:

        signal = "SELL"

        trend = "DOWN"

    else:

        signal = "WAIT"

        trend = "SIDE"

    # ======================
    # VOLATILITY
    # ======================

    if vol < 15:

        volatility = "LOW"

    elif vol < 40:

        volatility = "MEDIUM"

    else:

        volatility = "HIGH"

    # ======================
    # BIAS
    # ======================

    if score > 30:

        bias = "BULLISH"

    elif score < -30:

        bias = "BEARISH"

    else:

        bias = "NEUTRAL"

    # ======================
    # MARKET STATE
    # ======================

    if abs(ema20 - ema50) > 20:

        market_state = "TRENDING"

    elif volatility == "HIGH":

        market_state = "VOLATILE"

    else:

        market_state = "SIDEWAYS"

    # ======================
    # PROBABILITY
    # ======================

    probability = max(

        5,

        min(

            95,

            50 + score * 0.7

        )

    )

    # ======================
    # CONFIDENCE
    # ======================

    confidence = min(

        95,

        60 + abs(score) * 0.5

    )

    # ======================
    # SIGNAL MEMORY
    # ======================

    last_signal = signal

    last_candle = candle_start

    return {

        "signal": signal,

        "confidence":

            round(

                confidence,

                2

            ),

        "probability":

            round(

                probability,

                2

            ),

        "trend": trend,

        "market": "LIVE",

        "market_state":

            market_state,

        "bias":

            bias,

        "volatility":

            volatility,

        "risk":

            "LOW"

            if volatility == "LOW"

            else

            "MEDIUM"

            if volatility == "MEDIUM"

            else

            "HIGH",

        "strength":

            "STRONG"

            if abs(score) >= 60

            else

            "MEDIUM",

        "price":

            round(

                prices[-1],

                2

            ),

        "rsi":

            round(

                r,

                2

            ),

        "ema20":

            round(

                ema20,

                2

            ),

        "ema50":

            round(

                ema50,

                2

            ),

        "macd":

            round(

                m,

                4

            ),

        "timestamp":

            int(

                time.time()

            )

    }
