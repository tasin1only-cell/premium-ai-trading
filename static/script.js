console.log("LEVEL 8 FIXED JS LOADED");

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

    if (el) {
        el.innerText = `Candle Ends : 00:${String(remaining).padStart(2, "0")}`;
    }
}, 1000);

// ======================
// SAFE CHART
// ======================
function loadChart(symbol = "FX:EURUSD") {

    setTimeout(() => {
        try {
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
                locale: "en"
            });

        } catch (e) {
            console.log("Chart error", e);
        }
    }, 800);
}

// ======================
// UI
// ======================
function updateUI(data) {

    const rsi = data.rsi ?? 50;
    const price = data.price ?? 0;

    document.getElementById("signalBox").innerText =
        "SIGNAL : " + (data.signal || "WAIT");

    document.getElementById("trendBox").innerText =
        "TREND : " + (data.trend || "SIDE");

    document.getElementById("conf").innerText =
        "Confidence : " + (data.confidence || 50) + "%";

    const fill = document.getElementById("rsiFill");
    if (fill) fill.style.width = rsi + "%";

    const log = document.getElementById("historyLog");

    if (log) {
        const div = document.createElement("div");
        div.innerText =
            `${data.signal} | RSI ${rsi} | ${price}`;
        log.prepend(div);
    }
}

// ======================
// SIGNAL
// ======================
async function getSignal() {
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
// START
// ======================
function startBot() {
    if (started) return;
    started = true;

    getSignal();
    setInterval(getSignal, 60000);
}

// ======================
// INIT
// ======================
window.onload = () => {
    loadChart();
    startBot();
};
