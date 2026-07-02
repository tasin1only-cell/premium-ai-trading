console.log("AI TRADING PRO LEVEL 8B FIX LOADED");

const API_URL = "/api/signal";

let running = false;
let lastSignalTime = 0;
let lastHistorySignal = "";
let chartLoaded = false;

/* ================= CLOCK ================= */
setInterval(() => {
    const el = document.getElementById("clock");
    if (el) el.innerText = new Date().toLocaleTimeString();
}, 1000);

/* ================= CANDLE TIMER ================= */
setInterval(() => {
    const el = document.getElementById("candle");
    if (!el) return;

    const sec = new Date().getSeconds();
    const remaining = 60 - sec;

    el.innerText = `Candle Ends : 00:${String(remaining).padStart(2, "0")}`;
}, 1000);

/* ================= SAFE SET ================= */
function set(id, val) {
    const el = document.getElementById(id);
    if (el) el.innerText = val;
}

/* ================= CHART FIX (IMPORTANT LEVEL 8B) ================= */
function loadChart(symbol = "BINANCE:BTCUSDT") {

    const container = document.getElementById("tradingview_chart");
    if (!container) return;

    container.innerHTML = "";

    // IMPORTANT: delay ensures TradingView loads properly
    if (typeof TradingView === "undefined") {
        setTimeout(() => loadChart(symbol), 1200);
        return;
    }

    try {
        new TradingView.widget({
            container_id: "tradingview_chart",
            width: "100%",
            height: 350,
            symbol: symbol,
            interval: "1",
            theme: "dark",
            style: "1",
            locale: "en",
            autosize: true,
            hide_side_toolbar: true,
            allow_symbol_change: false
        });

        chartLoaded = true;

    } catch (e) {
        console.log("Chart Error:", e);
        chartLoaded = false;

        setTimeout(() => loadChart(symbol), 2000);
    }
}

/* ================= ASSET CHANGE ================= */
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

    loadChart(map[asset]);
}

/* ================= UI UPDATE ================= */
function updateUI(d) {

    set("signalBox", "SIGNAL : " + d.signal);
    set("trendBox", "TREND : " + d.trend);
    set("conf", "Confidence : " + d.confidence + "%");
    set("marketBox", "Market : " + d.market);
    set("riskBox", "Risk : " + d.risk);
    set("probBox", "Probability : " + d.probability + "%");
    set("strengthBox", "Strength : " + d.strength);

    const rsiFill = document.getElementById("rsiFill");
    if (rsiFill) rsiFill.style.width = d.rsi + "%";

    /* ================= HISTORY FIX (NO DUPLICATE SPAM) ================= */
    const now = Date.now();

    const newSignalKey = `${d.signal}_${d.rsi}_${Math.floor(d.price)}`;

    if (newSignalKey !== lastHistorySignal && now - lastSignalTime > 45000) {

        lastHistorySignal = newSignalKey;
        lastSignalTime = now;

        const log = document.getElementById("historyLog");

        if (log) {
            const div = document.createElement("div");
            div.innerText = `${d.signal} | RSI ${d.rsi} | Price ${d.price}`;
            log.prepend(div);

            while (log.childNodes.length > 15) {
                log.removeChild(log.lastChild);
            }
        }
    }
}

/* ================= API CALL (STABLE + RETRY) ================= */
async function getSignal() {

    if (running) return;
    running = true;

    try {
        const res = await fetch(API_URL + "?t=" + Date.now());

        if (!res.ok) throw new Error("API ERROR");

        const data = await res.json();

        if (data && data.signal) {
            updateUI(data);
        }

    } catch (e) {
        console.log("API FAIL - RETRYING", e);

        // retry after short delay
        setTimeout(() => {
            running = false;
        }, 1500);

        return;
    }

    setTimeout(() => {
        running = false;
    }, 900);
}

/* ================= BOT LOOP ================= */
function startBot() {

    getSignal();

    // stable fast refresh (safe for flask + render)
    setInterval(getSignal, 2000);
}

/* ================= INIT FIX ================= */
window.onload = () => {

    // chart must load after DOM + TV script
    setTimeout(() => {
        loadChart("BINANCE:BTCUSDT");
    }, 1800);

    startBot();
};
