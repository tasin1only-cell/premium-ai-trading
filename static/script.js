console.log("LEVEL 8 AI TRADING JS LOADED");

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
// CANDLE TIMER (SYNC FIX)
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
// CHART
// ======================
function loadChart(symbol = "FX:EURUSD") {

    setTimeout(() => {
        try {
            const chart = document.getElementById("tradingview_chart");
            if (!chart) return;

            chart.innerHTML = "";

            if (typeof TradingView === "undefined") {
                console.log("TradingView missing");
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
            console.log(err);
        }
    }, 700);
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
// UI UPDATE (LEVEL 8 READY)
// ======================
function updateUI(data) {

    const signalBox = document.getElementById("signalBox");
    const trendBox = document.getElementById("trendBox");
    const conf = document.getElementById("conf");
    const rsiFill = document.getElementById("rsiFill");
    const log = document.getElementById("historyLog");

    const rsi = data.rsi ?? 50;
    const price = data.price ?? 0;

    // ======================
    // SIGNAL
    // ======================
    if (signalBox) {
        signalBox.innerText = `SIGNAL : ${data.signal}`;

        signalBox.style.color =
            data.signal === "BUY" ? "#00ff66" :
            data.signal === "SELL" ? "#ff4444" :
            "gold";
    }

    // ======================
    // TREND
    // ======================
    if (trendBox) {
        trendBox.innerText = `TREND : ${data.trend || "SIDE"}`;
    }

    // ======================
    // CONFIDENCE + PROBABILITY
    // ======================
    if (conf) {
        conf.innerHTML =
            `Confidence : ${data.confidence || 50}%<br>
             Probability : ${data.probability || 0}%<br>
             Market : ${data.market || "UNKNOWN"}<br>
             Risk : ${data.risk || "UNKNOWN"}<br>
             Strength : ${data.strength || "NONE"}`;
    }

    // ======================
    // RSI BAR
    // ======================
    if (rsiFill) {
        rsiFill.style.width = rsi + "%";
        rsiFill.style.background =
            rsi > 70 ? "red" :
            rsi < 30 ? "lime" :
            "orange";
    }

    // ======================
    // HISTORY LOG
    // ======================
    if (log) {

        const item = document.createElement("div");

        item.style.padding = "4px";
        item.style.borderBottom = "1px solid #222";

        item.innerHTML =
            `<b>${data.signal}</b>
             | RSI ${rsi}
             | Price ${price}
             | Prob ${data.probability || 0}%
             | ${new Date().toLocaleTimeString()}`;

        log.prepend(item);

        while (log.childNodes.length > 15) {
            log.removeChild(log.lastChild);
        }
    }
}

// ======================
// SIGNAL ENGINE (CANDLE SYNC FIXED)
// ======================
async function generateSignal() {

    if (running) return;
    running = true;

    try {
        const res = await fetch(API_URL);
        const data = await res.json();

        updateUI(data);

    } catch (err) {
        console.log(err);
    }

    setTimeout(() => {
        running = false;
    }, 1500);
}

// ======================
// STRICT CANDLE SYNC (FIXED)
// ======================
function scheduleSignals() {

    const now = new Date();
    const sec = now.getSeconds();

    const delay = (60 - sec) * 1000;

    console.log("Next candle sync in", delay / 1000, "sec");

    setTimeout(() => {

        generateSignal();

        setInterval(() => {
            const secNow = new Date().getSeconds();

            if (secNow === 0) {
                generateSignal();
            }

        }, 1000);

    }, delay);
}

// ======================
// START BOT
// ======================
function startBot() {
    if (started) return;
    started = true;

    scheduleSignals();
}

// ======================
// DEBUG CANDLES
// ======================
async function loadCandles() {
    try {
        const res = await fetch(CANDLE_URL);
        const data = await res.json();
        console.log("CANDLES:", data.slice(-3));
    } catch (err) {}
}

// ======================
// INIT
// ======================
window.onload = () => {

    loadChart("FX:EURUSD");

    startBot();

    setInterval(loadCandles, 30000);
};
