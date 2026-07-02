console.log("LEVEL 9 STABLE AI TRADING JS");

// ======================
// API
// ======================
const API_URL = "/api/signal";

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
function updateCandleTimer() {
    const now = new Date();
    const sec = now.getSeconds();
    const remaining = 60 - sec;

    const el = document.getElementById("candle");
    if (el) {
        el.innerText = `Candle Ends : 00:${String(remaining).padStart(2, "0")}`;

        el.style.color =
            remaining <= 5 ? "red" :
            remaining <= 15 ? "orange" :
            "#00ff99";
    }
}
setInterval(updateCandleTimer, 1000);

// ======================
// SAFE CHART LOADER (FIXED)
// ======================
function loadChart(symbol = "FX:EURUSD") {

    setTimeout(() => {

        const el = document.getElementById("tradingview_chart");
        if (!el) return;

        // IMPORTANT: prevent overwrite bug
        el.innerHTML = "";

        if (typeof TradingView === "undefined") {
            console.log("TradingView not loaded yet");
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

    }, 1200); // 🔥 important delay fix
}

// ======================
// UI UPDATE
// ======================
function updateUI(data) {

    const signalBox = document.getElementById("signalBox");
    const trendBox = document.getElementById("trendBox");
    const conf = document.getElementById("conf");
    const rsiFill = document.getElementById("rsiFill");
    const log = document.getElementById("historyLog");

    const rsi = data.rsi ?? 50;
    const price = data.price ?? 0;

    if (signalBox) {
        signalBox.innerText = "SIGNAL : " + (data.signal || "WAIT");

        signalBox.style.color =
            data.signal === "BUY" ? "#00ff66" :
            data.signal === "SELL" ? "#ff4444" :
            "gold";
    }

    if (trendBox) {
        trendBox.innerText = "TREND : " + (data.trend || "SIDE");
    }

    if (conf) {
        conf.innerText = "Confidence : " + (data.confidence || 50) + "%";
    }

    if (rsiFill) {
        rsiFill.style.width = rsi + "%";
    }

    if (log) {
        const div = document.createElement("div");
        div.innerText = `${data.signal} | RSI ${rsi} | Price ${price} | ${new Date().toLocaleTimeString()}`;

        log.prepend(div);

        while (log.childNodes.length > 15) {
            log.removeChild(log.lastChild);
        }
    }
}

// ======================
// SIGNAL ENGINE (CANDLE SYNC FIX)
// ======================
async function getSignal() {

    if (running) return;
    running = true;

    try {
        const res = await fetch(API_URL);
        const data = await res.json();

        console.log("SIGNAL:", data);

        updateUI(data);

    } catch (err) {
        console.log(err);
    }

    setTimeout(() => {
        running = false;
    }, 2000);
}

// ======================
// START BOT (CANDLE ALIGNED)
// ======================
function startBot() {

    if (started) return;
    started = true;

    // 🔥 align to candle start
    const now = new Date();
    const delay = (60 - now.getSeconds()) * 1000;

    console.log("Sync start in", delay / 1000, "sec");

    setTimeout(() => {

        getSignal();
        setInterval(getSignal, 60000);

    }, delay);
}

// ======================
// INIT (FIX ORDER)
// ======================
window.onload = () => {

    console.log("LEVEL 9 READY");

    loadChart("FX:EURUSD");

    startBot();
};
