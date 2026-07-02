console.log("STABLE AI SYSTEM LOADED");

const API = "/api/signal";
const STATUS = "/api/status";

let lastCandle = 0;
let running = false;

/* CLOCK */
setInterval(() => {
    const el = document.getElementById("clock");
    if (el) el.innerText = new Date().toLocaleTimeString();
}, 1000);

/* CANDLE SYNC (ONLY ON NEW CANDLE) */
async function checkCandle() {
    try {
        const res = await fetch(STATUS);
        const data = await res.json();

        if (data.candle_start !== lastCandle) {
            lastCandle = data.candle_start;
            fetchSignal(); // ONLY ON NEW CANDLE
        }
    } catch (e) {}
}

setInterval(checkCandle, 3000);

/* SIGNAL FETCH (ANTI SPAM) */
async function fetchSignal() {
    if (running) return;
    running = true;

    try {
        const res = await fetch(API);
        const data = await res.json();

        if (!data || data.market === "WARMUP") return;

        updateUI(data);

    } catch (e) {
        console.log(e);
    }

    setTimeout(() => running = false, 1500);
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
        div.innerText = `${data.signal} | RSI ${rsi} | ${data.price}`;
        log.prepend(div);
    }
}

/* START */
window.onload = () => {
    fetchSignal();
};
