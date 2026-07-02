console.log("LEVEL 8 FIXED SYSTEM LOADED");

const API_URL = "/api/signal";

let running = false;
let started = false;

/* CLOCK */
setInterval(() => {
    const el = document.getElementById("clock");
    if (el) el.innerText = new Date().toLocaleTimeString();
}, 1000);

/* CANDLE SYNC */
function getCandleRemaining() {
    return 60 - new Date().getSeconds();
}

setInterval(() => {
    const el = document.getElementById("candle");
    if (!el) return;

    const remaining = getCandleRemaining();

    el.innerText = `Candle Ends : 00:${String(remaining).padStart(2,"0")}`;

    el.style.color =
        remaining <= 5 ? "red" :
        remaining <= 15 ? "orange" :
        "#ffcc00";

}, 1000);

/* CHART */
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

/* UI */
function updateUI(data) {

    const rsi = data.rsi ?? 50;
    const price = data.price ?? 0;

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

/* SIGNAL */
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

/* START */
function startBot() {

    if (started) return;
    started = true;

    generateSignal();

    setInterval(() => {
        generateSignal();
    }, 60000);
}

/* INIT */
window.onload = () => {
    loadChart();
    startBot();
};
