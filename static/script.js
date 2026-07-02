console.log("STABLE RESET PACK LOADED");

const API_URL = "/api/signal";
const STATUS_URL = "/api/status";

let lastCandle = 0;
let running = false;

/* CLOCK */
setInterval(() => {
    const el = document.getElementById("clock");
    if (el) el.innerText = new Date().toLocaleTimeString();
}, 1000);

/* CANDLE SYNC (REAL FIX) */
async function syncCandle() {
    try {
        const res = await fetch(STATUS_URL);
        const data = await res.json();

        if (data.candle_start !== lastCandle) {
            lastCandle = data.candle_start;
            getSignal(); // only new candle
        }

    } catch (e) {}
}

setInterval(syncCandle, 3000);

/* SIGNAL */
async function getSignal() {

    if (running) return;
    running = true;

    try {
        const res = await fetch(API_URL);
        const data = await res.json();

        if (!data || !data.price) {
            running = false;
            return;
        }

        updateUI(data);

    } catch (e) {
        console.log(e);
    }

    setTimeout(() => running = false, 1000);
}

/* UI SAFE */
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
    setInterval(getSignal, 15000); // safe refresh
};
