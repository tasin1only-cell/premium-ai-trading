console.log("LEVEL 6C PRO JS LOADED");

// ======================
// API
// ======================
const API_URL = "https://premium-ai-trading.onrender.com/api/signal";

// ======================
// STATE CONTROL
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
// VISUAL CANDLE TIMER (SYNC IMPROVED)
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
// TRADINGVIEW CHART
// ======================
let widget = null;

function loadChart(symbol = "FX:EURUSD") {
    try {
        const chart = document.getElementById("tradingview_chart");

        if (!chart) return;

        chart.innerHTML = "";

        widget = new TradingView.widget({
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
}


// ======================
// ASSET CHANGE FIX
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
// UI UPDATE ENGINE (CLEAN)
// ======================
function updateUI(data) {

    const signalBox = document.getElementById("signalBox");
    const trendBox = document.getElementById("trendBox");
    const conf = document.getElementById("conf");
    const rsiFill = document.getElementById("rsiFill");
    const log = document.getElementById("historyLog");

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
        trendBox.innerText = "TREND: " + data.trend;

        trendBox.style.color =
            data.trend === "UP" ? "#00ff66" :
            data.trend === "DOWN" ? "#ff4444" :
            "gold";
    }

    // CONFIDENCE
    if (conf) {
        conf.innerText = "Confidence : " + data.confidence + "%";

        conf.style.color =
            data.confidence > 70 ? "#00ff66" :
            data.confidence < 40 ? "#ff4444" :
            "gold";
    }

    // RSI BAR
    if (rsiFill) {
        rsiFill.style.width = data.rsi + "%";

        rsiFill.style.background =
            data.rsi > 70 ? "red" :
            data.rsi < 30 ? "lime" :
            "orange";
    }

    // HISTORY
    if (log) {

        const item = document.createElement("div");

        item.style.padding = "4px";
        item.style.borderBottom = "1px solid #222";

        item.innerText =
            `${data.signal} | RSI ${data.rsi} | P ${data.price} | ${new Date().toLocaleTimeString()}`;

        log.prepend(item);

        while (log.childNodes.length > 15) {
            log.removeChild(log.lastChild);
        }
    }
}


// ======================
// SIGNAL ENGINE (STABLE PRO)
// ======================
async function generateSignal() {

    if (running) return;

    running = true;

    try {

        const res = await fetch(API_URL);

        if (!res.ok) throw new Error("API ERROR");

        const data = await res.json();

        console.log("DATA:", data);

        updateUI(data);

    } catch (err) {
        console.log("ERROR:", err);
    }

    setTimeout(() => {
        running = false;
    }, 1200);
}


// ======================
// AUTO START (FIXED)
// ======================
function startBot() {

    if (started) return;

    started = true;

    generateSignal();

    setInterval(generateSignal, 60000); // 1 minute candle sync
}


// ======================
// INIT
// ======================
window.onload = () => {

    console.log("PAGE LOADED");

    loadChart("FX:EURUSD");

    startBot();
};
