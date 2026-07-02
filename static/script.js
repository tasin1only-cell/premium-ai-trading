console.log("LEVEL 8 FINAL SYSTEM LOADED");

const API_URL = "/api/signal";
const STATUS_URL = "/api/status";

let lastCandle = 0;

/* CLOCK */
setInterval(() => {
    const el = document.getElementById("clock");
    if (el) el.innerText = new Date().toLocaleTimeString();
}, 1000);

/* CANDLE SYNC ENGINE */
async function syncCandle() {
    try {
        const res = await fetch(STATUS_URL);
        const data = await res.json();

        if (data.candle_start !== lastCandle) {
            lastCandle = data.candle_start;
            getSignal(); // new candle only
        }

    } catch (e) {}
}

setInterval(syncCandle, 3000);

/* SIGNAL */
async function getSignal() {
    try {
        const res = await fetch(API_URL);
        const data = await res.json();
        updateUI(data);
    } catch (e) {
        console.log(e);
    }
}

/* UI */
function updateUI(data) {

    const set = (id, val) => {
        const el = document.getElementById(id);
        if (el) el.innerText = val;
    };

    set("signalBox", "SIGNAL : " + data.signal);
    set("trendBox", "TREND : " + data.trend);
    set("conf", "Confidence : " + data.confidence + "%");
    set("marketBox", "Market : " + data.market);
    set("riskBox", "Risk : " + data.risk);
    set("probBox", "Probability : " + data.probability + "%");
    set("strengthBox", "Strength : " + data.strength);

    const rsi = data.rsi ?? 50;
    const fill = document.getElementById("rsiFill");
    if (fill) fill.style.width = rsi + "%";

    const log = document.getElementById("historyLog");

    if (log) {
        const div = document.createElement("div");
        div.innerText =
            `${data.signal} | RSI ${rsi} | Price ${data.price} | ${new Date().toLocaleTimeString()}`;

        log.prepend(div);

        while (log.childNodes.length > 15) {
            log.removeChild(log.lastChild);
        }
    }
}

/* INIT */
window.onload = () => {
    getSignal();
    setInterval(getSignal, 60000);
};
