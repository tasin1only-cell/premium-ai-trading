console.log("AI TRADING PRO STABLE SYSTEM LOADED");

const API_URL = "/api/signal";

let running = false;
let started = false;
let lastCandleSecond = -1;

/* ======================
   CLOCK
====================== */
setInterval(() => {
    const el = document.getElementById("clock");
    if (el) el.innerText = new Date().toLocaleTimeString();
}, 1000);


/* ======================
   REAL CANDLE SYNC (FIXED)
   → ONLY triggers at new minute
====================== */
function getMinute() {
    return new Date().getMinutes();
}

let lastMinute = getMinute();

function candleWatcher() {
    const nowMin = getMinute();

    if (nowMin !== lastMinute) {
        lastMinute = nowMin;
        generateSignal(); // ONLY new candle
    }

    // UI timer
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
}

setInterval(candleWatcher, 1000);


/* ======================
   SAFE CHART LOADER
====================== */
function loadChart(symbol = "FX:EURUSD") {

    setTimeout(() => {
        const el = document.getElementById("tradingview_chart");
        if (!el) return;

        el.innerHTML = "";

        if (!window.TradingView) return;

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

    }, 500);
}


/* ======================
   ASSET CHANGE (IMPORTANT FIX)
====================== */
function changeAsset() {

    const val = document.getElementById("asset").value;

    const map = {
        "EUR/USD": "FX:EURUSD",
        "GBP/USD": "FX:GBPUSD",
        "USD/JPY": "FX:USDJPY",
        "BTC/USD": "BINANCE:BTCUSDT",
        "ETH/USD": "BINANCE:ETHUSDT",
        "XAU/USD": "OANDA:XAUUSD"
    };

    loadChart(map[val] || "FX:EURUSD");

    // reset candle sync so signal aligns
    lastMinute = getMinute();
    generateSignal();
}


/* ======================
   UI UPDATE (SAFE + FULL)
====================== */
function updateUI(data) {

    const set = (id, val) => {
        const el = document.getElementById(id);
        if (el) el.innerText = val;
    };

    set("signalBox", "SIGNAL : " + (data.signal || "WAIT"));
    set("trendBox", "TREND : " + (data.trend || "SIDE"));
    set("conf", "Confidence : " + (data.confidence || 50) + "%");

    set("marketBox", "Market : " + (data.market || "UNKNOWN"));
    set("riskBox", "Risk : " + (data.risk || "LOW"));
    set("probBox", "Probability : " + (data.probability || 0) + "%");
    set("strengthBox", "Strength : " + (data.strength || "NONE"));

    // RSI BAR
    const rsi = data.rsi ?? 50;
    const fill = document.getElementById("rsiFill");
    if (fill) fill.style.width = rsi + "%";

    // HISTORY
    const log = document.getElementById("historyLog");

    if (log) {
        const div = document.createElement("div");
        div.innerText =
            `${data.signal} | RSI ${rsi.toFixed(2)} | Price ${data.price} | Prob ${data.probability ?? 0}%`;

        log.prepend(div);

        while (log.childNodes.length > 15) {
            log.removeChild(log.lastChild);
        }
    }
}


/* ======================
   SIGNAL FETCH
====================== */
async function generateSignal() {

    if (running) return;
    running = true;

    try {
        const res = await fetch(API_URL);
        const data = await res.json();

        // IMPORTANT: ignore warmup crash state
        if (!data || data.market === "WARMUP") {
            console.log("WARMUP STATE - waiting real candle");
            return;
        }

        updateUI(data);

    } catch (e) {
        console.log("API ERROR", e);
    }

    setTimeout(() => running = false, 1200);
}


/* ======================
   INIT
====================== */
window.onload = () => {

    loadChart();

    // start chart + sync
    generateSignal();
    setInterval(generateSignal, 10000); // safety fallback (UI refresh)

};
