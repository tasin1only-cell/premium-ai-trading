console.log("FINAL LEVEL 8 SYNC SYSTEM LOADED");

const API_URL = "/api/signal";

let running = false;
let started = false;
let chartLoaded = false;

/* ================= CLOCK ================= */
setInterval(() => {
    const el = document.getElementById("clock");
    if (el) el.innerText = new Date().toLocaleTimeString();
}, 1000);

/* ================= CANDLE TIMER (PURE UI ONLY) ================= */
setInterval(() => {
    const el = document.getElementById("candle");
    if (!el) return;

    const sec = new Date().getSeconds();
    const remaining = 60 - sec;

    el.innerText = `Candle Ends : 00:${String(remaining).padStart(2,"0")}`;
}, 1000);

/* ================= CHART FIX ================= */
function loadChart(symbol = "FX:EURUSD") {

    const el = document.getElementById("tradingview_chart");
    if (!el) return;

    el.innerHTML = "";

    setTimeout(() => {

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
            allow_symbol_change: false,
            autosize: true
        });

        chartLoaded = true;

    }, 1000);
}

/* ================= ASSET ================= */
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

/* ================= UI ================= */
function set(id, val) {
    const el = document.getElementById(id);
    if (el) el.innerText = val;
}

/* ================= UPDATE ================= */
function updateUI(d) {

    set("signalBox", "SIGNAL : " + (d.signal || "WAIT"));
    set("trendBox", "TREND : " + (d.trend || "SIDE"));
    set("conf", "Confidence : " + (d.confidence ?? 50) + "%");

    set("marketBox", "Market : " + (d.market || "UNKNOWN"));
    set("riskBox", "Risk : " + (d.risk || "LOW"));
    set("probBox", "Probability : " + (d.probability ?? 0) + "%");
    set("strengthBox", "Strength : " + (d.strength || "NONE"));

    const rsi = d.rsi ?? 50;
    const price = d.price ?? 0;

    const fill = document.getElementById("rsiFill");
    if (fill) fill.style.width = rsi + "%";

    const log = document.getElementById("historyLog");

    if (log) {

        const time = new Date(d.timestamp ? d.timestamp * 1000 : Date.now())
            .toLocaleTimeString();

        const div = document.createElement("div");

        div.innerText =
            `${d.signal} | RSI ${rsi} | Price ${price} | ${time}`;

        log.prepend(div);

        while (log.childNodes.length > 15) {
            log.removeChild(log.lastChild);
        }
    }
}

/* ================= SIGNAL ENGINE (SYNC FIX CORE) ================= */
async function getSignal() {

    if (running) return;
    running = true;

    try {
        const res = await fetch(API_URL + "?t=" + Date.now());
        const data = await res.json();

        updateUI(data);

    } catch (e) {
        console.log("API ERROR", e);
    }

    setTimeout(() => running = false, 1000);
}

/* ================= START ================= */
function startBot() {

    if (started) return;
    started = true;

    getSignal();

    // 🔥 FIX: faster sync = candle mismatch solve
    setInterval(getSignal, 5000);
}

/* ================= INIT ================= */
window.onload = () => {

    loadChart();
    startBot();

};
