from flask import Flask, jsonify, render_template
from flask_cors import CORS
import threading
import time
import random
from ai_engine import ai_engine

app = Flask(__name__)
CORS(app)

prices = []
candle_start = int(time.time() // 60)  # IMPORTANT FIX

def price_loop():
    price = 100

    while True:
        price += random.uniform(-1.2, 1.2)
        prices.append(price)

        if len(prices) > 2000:
            prices.pop(0)

        time.sleep(1)

# ======================
# SIGNAL API
# ======================
@app.route("/api/signal")
def signal():
    return jsonify(ai_engine(prices))

# ======================
# STATUS (IMPORTANT FOR SYNC)
# ======================
@app.route("/api/status")
def status():
    global candle_start
    return jsonify({
        "candle_start": candle_start,
        "server_time": int(time.time())
    })

@app.route("/")
def home():
    return render_template("index.html")

threading.Thread(target=price_loop, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
