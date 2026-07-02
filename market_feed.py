import websocket
import json
import threading

prices = []

def on_message(ws, message):
    global prices

    data = json.loads(message)

    if "k" in data:

        candle = data["k"]

        close_price = float(candle["c"])

        prices.append(close_price)

        if len(prices) > 2000:
            prices.pop(0)


def on_error(ws, error):
    print("WS ERROR:", error)


def on_close(ws, a, b):
    print("WS CLOSED")


def on_open(ws):
    print("CONNECTED TO BINANCE")


def start_feed():

    socket = (
        "wss://stream.binance.com:9443/ws/"
        "btcusdt@kline_1m"
    )

    ws = websocket.WebSocketApp(

        socket,

        on_message=on_message,

        on_error=on_error,

        on_close=on_close

    )

    ws.on_open = on_open

    ws.run_forever()


threading.Thread(
    target=start_feed,
    daemon=True
).start()
