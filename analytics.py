import time

trade_log = []


def log_signal(signal, price, rsi, outcome=None):
    trade_log.append({
        "signal": signal,
        "price": price,
        "rsi": rsi,
        "time": time.time(),
        "outcome": outcome  # later evaluation
    })

    if len(trade_log) > 200:
        trade_log.pop(0)


def calculate_winrate():
    if len(trade_log) < 10:
        return {
            "buy_winrate": 50,
            "sell_winrate": 50,
            "total": len(trade_log)
        }

    buy = [t for t in trade_log if t["signal"] == "BUY"]
    sell = [t for t in trade_log if t["signal"] == "SELL"]

    buy_win = [t for t in buy if t["outcome"] == "WIN"]
    sell_win = [t for t in sell if t["outcome"] == "WIN"]

    return {
        "buy_winrate": round((len(buy_win) / len(buy) * 100), 2) if buy else 50,
        "sell_winrate": round((len(sell_win) / len(sell) * 100), 2) if sell else 50,
        "total_signals": len(trade_log),
        "buy_count": len(buy),
        "sell_count": len(sell)
    }
