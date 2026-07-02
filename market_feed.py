import websocket
import json
import threading
import time

prices = []
lock = threading.Lock()

socket_url = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"


# ==========================
# SAFE PRICE PUSH
# ==========================
def push_price(price):

    global prices

    with lock:

        if len(prices) > 0:

            # prevent duplicate same candle spam
            if abs(prices[-1] - price) < 0.00001:
                return

        prices.append(price)

        if len(prices) > 2000:
            prices.pop(0)


# ==========================
# MESSAGE HANDLER
# ==========================
def on_message(ws, message):

    try:
        data = json.loads(message)

        if "k" not in data:
            return

        candle = data["k"]

        close_price = candle.get("c", None)

        if close_price is None:
            return

        price = float(close_price)

        push_price(round(price, 2))

    except Exception as e:
        print("WS PARSE ERROR:", e)


# ==========================
# ERROR HANDLER
# ==========================
def on_error(ws, error):
    print("WS ERROR:", error)


# ==========================
# CLOSE HANDLER (AUTO RECONNECT TRIGGER)
# ==========================
def on_close(ws, a, b):
    print("WS CLOSED - RECONNECTING IN 3s")
    time.sleep(3)
    start_feed()


# ==========================
# OPEN HANDLER
# ==========================
def on_open(ws):
    print("CONNECTED TO BINANCE LIVE FEED")


# ==========================
# START FEED (AUTO RECONNECT SAFE)
# ==========================
def start_feed():

    ws = websocket.WebSocketApp(
        socket_url,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open
    )

    ws.run_forever(
        ping_interval=20,
        ping_timeout=10
    )


# ==========================
# BACKGROUND THREAD START
# ==========================
def start_background():

    thread = threading.Thread(
        target=start_feed,
        daemon=True
    )

    thread.start()


# AUTO START
start_background()
