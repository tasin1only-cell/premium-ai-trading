console.log("LEVEL 9 SYNC SYSTEM LOADED");

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
// CANDLE TIMER (SYNC REAL)
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
// CHART
// ======================
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
            locale: "en"
        });
    }, 700);
}

// ======================
// UI UPDATE
// ======================
function updateUI(data) {

    const rsi = data.rsi ?? 50;
    const price = data.price ?? 0;

    document.getElementById("signalBox").innerText =
        "SIGNAL : " + data.signal;

    document.getElementById("trendBox").innerText =
        "TREND : " + data.trend;

    document.getElementById("conf").innerText =
        "Confidence : " + data.confidence + "%";

    document.getElementById("marketBox").innerText =
        "Market : " + data.market;

    document.getElementById("riskBox").innerText =
        "Risk : " + data.risk;

    document.getElementById("probBox").innerText =
        "Probability : " + data.probability + "%";

    document.getElementById("strengthBox").innerText =
        "Strength : " + data.strength;

    const fill = document.getElementById("rsiFill");
    if (fill) fill.style.width = rsi + "%";

    const log = document.getElementById("historyLog");

    if (log) {
        const time = data.timestamp
            ? new Date(data.timestamp * 1000).toLocaleTimeString()
            : new Date().toLocaleTimeString();

        const div = document.createElement("div");
        div.innerText =
            `${time} | ${data.signal} | RSI ${rsi} | Price ${price} | Prob ${data.probability}%`;

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
// START (CANDLE SYNC FIX)
// ======================
function startBot() {

    if (started) return;
    started = true;

    const run = () => generateSignal();

    const sec = new Date().getSeconds();
    const delay = (60 - sec) * 1000;

    setTimeout(() => {
        run();
        setInterval(run, 60000);
    }, delay);
}

// ======================
// INIT
// ======================
window.onload = () => {
    loadChart();
    startBot();
};
