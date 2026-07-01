def analyze(rsi, macd, ema):

    score = 0

    # RSI
    if rsi > 55:
        score += 1

    elif rsi < 45:
        score -= 1


    # MACD
    if macd == "BUY":
        score += 1

    elif macd == "SELL":
        score -= 1


    # EMA
    if ema == "UP":
        score += 1

    elif ema == "DOWN":
        score -= 1


    confidence = 50 + abs(score) * 15


    if score > 0:

        signal = "BUY"

    elif score < 0:

        signal = "SELL"

    else:

        signal = "WAIT"


    return {

        "signal": signal,

        "confidence": confidence,

        "score": score

    }
