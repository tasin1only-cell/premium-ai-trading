def analyze(rsi, macd, ema):

    score = 0

    # RSI logic
    if rsi > 60:
        score += 1
    elif rsi < 40:
        score -= 1

    # MACD logic
    if macd == "BUY":
        score += 1
    elif macd == "SELL":
        score -= 1

    # EMA logic
    if ema == "UP":
        score += 1
    elif ema == "DOWN":
        score -= 1

    # Final decision
    if score >= 2:
        return "BUY"
    elif score <= -2:
        return "SELL"
    else:
        return "WAIT"