
console.log("LEVEL 7 AI TRADING JS LOADED");

// ======================
// API
// ======================
const API_URL = "/api/signal";
const CANDLE_URL = "/api/candles";

// ======================
// STATE
// ======================
let running = false;
let started = false;

// ======================
// CLOCK
// ======================
setInterval(() => {
    const el = document.getElementById("clock");
    if (el) el.innerText = new Date().toLocaleTimeString();
}, 1000);

// ======================
// CANDLE TIMER UI
// ======================
setInterval(() => {
    const sec = new Date().getSeconds();
    const remaining = 60 - sec;

    const el = document.getElementById("candle");

    if (el) {
        el.innerText = `Candle Ends : 00:${String(remaining).padStart(2, "0")}`;

        el.style.color =
            remaining <= 5 ? "red" :
            remaining <= 15 ? "orange" :
            "#ffcc00";
    }
}, 1000);

// ======================
// TRADINGVIEW CHART (FIXED STABLE)
// ======================
function loadChart(symbol = "FX:EURUSD") {

    setTimeout(() => {
        try {

            const chart = document.getElementById("tradingview_chart");

            if (!chart) {
                console.log("Chart container missing");
                return;
            }

            chart.innerHTML = "";

            if (typeof TradingView === "undefined") {
                console.log("TradingView not loaded");
                return;
            }

            new TradingView.widget({
                container_id: "tradingview_chart",
                width: "100%",
                height: 320,
                symbol: symbol,
                interval: "1",
                theme: "dark",
                style: "1",
                locale: "en",
                hide_side_toolbar: true,
                allow_symbol_change: false
            });

        } catch (err) {
            console.log("Chart Error:", err);
        }

    }, 800); // 🔥 IMPORTANT DELAY FIX
}

// ======================
// ASSET SWITCH
// ======================
function changeAsset() {

    const asset = document.getElementById("asset").value;

    const map = {
        "EUR/USD": "FX:EURUSD",
        "GBP/USD": "FX:GBPUSD",
        "USD/JPY": "FX:USDJPY",
        "BTC/USD": "BINANCE:BTCUSDT",
        "ETH/USD": "BINANCE:ETHUSDT",
        "XAU/USD": "OANDA:XAUUSD"
    };

    loadChart(map[asset] || "FX:EURUSD");
}

// ======================
// UI UPDATE ENGINE (SAFE)
// ======================
function updateUI(data) {

    const signalBox = document.getElementById("signalBox");
    const trendBox = document.getElementById("trendBox");
    const conf = document.getElementById("conf");
    const rsiFill = document.getElementById("rsiFill");
    const log = document.getElementById("historyLog");

    // SAFE fallback
    const rsi = data.rsi ?? 50;
    const price = data.price ?? 0;

    // SIGNAL
    if (signalBox) {
        signalBox.innerText = "SIGNAL : " + data.signal;

        signalBox.style.color =
            data.signal === "BUY" ? "#00ff66" :
            data.signal === "SELL" ? "#ff4444" :
            "gold";
    }

    // TREND
    if (trendBox) {
        trendBox.innerText = "TREND: " + (data.trend || "SIDE");

        trendBox.style.color =
            data.trend === "UP" ? "#00ff66" :
            data.trend === "DOWN" ? "#ff4444" :
            "gold";
    }

    // CONFIDENCE
    if (conf) {
        conf.innerText = "Confidence : " + (data.confidence || 50) + "%";

        conf.style.color =
            data.confidence > 70 ? "#00ff66" :
            data.confidence < 40 ? "#ff4444" :
            "gold";
    }

    // RSI BAR
    if (rsiFill) {
        rsiFill.style.width = rsi + "%";

        rsiFill.style.background =
            rsi > 70 ? "red" :
            rsi < 30 ? "lime" :
            "orange";
    }

    // HISTORY LOG
    if (log) {

        const item = document.createElement("div");

        item.innerText =
            `${data.signal} | RSI ${rsi} | Price ${price} | ${new Date().toLocaleTimeString()}`;

        log.prepend(item);

        while (log.childNodes.length > 15) {
            log.removeChild(log.lastChild);
        }
    }
}

// ======================
// SIGNAL ENGINE (STABLE)
// ======================
async function generateSignal() {

    if (running) return;

    running = true;

    try {

        const res = await fetch(API_URL);

        if (!res.ok) throw new Error("API ERROR");

        const data = await res.json();

        console.log("SIGNAL:", data);

        updateUI(data);

    } catch (err) {
        console.log("ERROR:", err);
    }

    setTimeout(() => {
        running = false;
    }, 1500);
}

// ======================
// AUTO START BOT
// ======================
function startBot() {

    if (started) return;

    started = true;

    generateSignal();

    setInterval(generateSignal, 60000);
}

// ======================
// REAL CANDLE DEBUG (OPTIONAL)
// ======================
async function loadCandles() {
    try {
        const res = await fetch(CANDLE_URL);
        const data = await res.json();
        console.log("CANDLES:", data.slice(-3));
    } catch (err) {
        console.log("CANDLE ERROR:", err);
    }
}

// ======================
// INIT (FIXED ORDER)
// ======================
window.onload = () => {

    console.log("LEVEL 7 DASHBOARD READY");

    setTimeout(() => {
        loadChart("FX:EURUSD");
    }, 500);

    startBot();

    setInterval(loadCandles, 30000);
};
