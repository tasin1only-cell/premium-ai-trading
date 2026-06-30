from flask import Flask, request, jsonify
from flask_cors import CORS
from ai_engine import analyze

app = Flask(__name__)
CORS(app)

# Home route (test)
@app.route("/")
def home():
    return "AI Server Running Successfully"

# Main AI prediction route
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json

        rsi = data.get("rsi")
        macd = data.get("macd")
        ema = data.get("ema")

        result = analyze(rsi, macd, ema)

        return jsonify({
            "signal": result,
            "confidence": 75
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)