console.log("LEVEL 8 FULL FIX SYSTEM LOADED");

const API_URL = "/api/signal";

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
// CANDLE TIMER (SYNC)
// ======================
setInterval(() => {
    const sec = new Date().getSeconds();
    const remaining = 60 - sec;

    const el = document.getElementById("candle");
    if (!el) return;

    el.innerText = `Candle Ends : 00:${String(remaining).padStart(2, "0")}`;

    el.style.color =
        remaining <= 5 ? "red" :
        remaining <= 15 ? "orange" :
        "#ffcc00";

}, 1000);

// ======================
// ASSET MAP (IMPORTANT FIX)
// ======================
const assetMap = {
    "EUR/USD": "FX:EURUSD",
    "GBP/USD": "FX:GBPUSD",
    "USD/JPY": "FX:USDJPY",
    "BTC/USD": "BINANCE:BTCUSDT",
    "ETH/USD": "BINANCE:ETHUSDT",
    "XAU/USD": "OANDA:XAUUSD"
};

// ======================
// CURRENT SYMBOL STATE
// ======================
let currentSymbol = "FX:EURUSD";

// ======================
// CHART LOAD (FULL RESET FIX)
// ======================
function loadChart(symbol) {

    currentSymbol = symbol;

    setTimeout(() => {
        const el = document.getElementById("tradingview_chart");
        if (!el) return;

        // 🔥 IMPORTANT CLEAN RESET
        el.innerHTML = "";

        if (!window.TradingView) {
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

    }, 600);
}

// ======================
// FIXED ASSET CHANGE (MAIN FIX)
// ======================
function changeAsset() {
    const asset = document.getElementById("asset").value;
    const symbol = assetMap[asset] || "FX:EURUSD";

    console.log("ASSET CHANGED →", asset, symbol);

    loadChart(symbol);
}

// ======================
// UI UPDATE
// ======================
function updateUI(data) {

    const set = (id, val) => {
        const el = document.getElementById(id);
        if (el) el.innerText = val;
    };

    set("signalBox", "SIGNAL : " + (data.signal || "WAIT"));
    set("trendBox", "TREND : " + (data.trend || "SIDE"));
    set("conf", "Confidence : " + (data.confidence || 50) + "%");

    set("marketBox", "Market : " + (data.market || "UNKNOWN"));
    set("riskBox", "Risk : " + (data.risk || "UNKNOWN"));
    set("probBox", "Probability : " + (data.probability || 0) + "%");
    set("strengthBox", "Strength : " + (data.strength || "NONE"));

    const rsi = data.rsi ?? 50;
    const price = data.price ?? 0;

    const fill = document.getElementById("rsiFill");
    if (fill) fill.style.width = rsi + "%";

    const log = document.getElementById("historyLog");

    if (log) {
        const div = document.createElement("div");
        div.innerText =
            `${data.signal} | RSI ${rsi} | Price ${price} | Prob ${data.probability ?? 0}%`;

        log.prepend(div);

        while (log.childNodes.length > 15) {
            log.removeChild(log.lastChild);
        }
    }
}

// ======================
// SIGNAL FETCH
// ======================
async function generateSignal() {

    if (running) return;
    running = true;

    try {
        const res = await fetch(API_URL);
        const data = await res.json();

        updateUI(data);

    } catch (e) {
        console.log(e);
    }

    setTimeout(() => running = false, 1200);
}

// ======================
// START BOT (SYNC SAFE)
// ======================
function startBot() {

    if (started) return;
    started = true;

    generateSignal();

    setInterval(() => {
        generateSignal();
    }, 60000);
}

// ======================
// INIT
// ======================
window.onload = () => {

    loadChart(currentSymbol); // 🔥 FIXED INIT

    startBot();

    // 🔥 AUTO HOOK for asset dropdown (important fix)
    const asset = document.getElementById("asset");
    if (asset) {
        asset.addEventListener("change", changeAsset);
    }
};
