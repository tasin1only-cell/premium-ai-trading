console.log("STABLE RESET PACK LOADED");

const API = "/api/signal";
const STATUS = "/api/status";

let lastCandle = 0;

/* CLOCK */
setInterval(() => {
    const el = document.getElementById("clock");
    if (el) el.innerText = new Date().toLocaleTimeString();
}, 1000);


/* CANDLE SYNC (REAL FIX) */
setInterval(async () => {
    try {
        const res = await fetch(STATUS);
        const data = await res.json();

        if (data.candle_start !== lastCandle) {
            lastCandle = data.candle_start;
            fetchSignal();
        }

    } catch (e) {}
}, 3000);


/* SIGNAL */
async function fetchSignal() {
    try {
        const res = await fetch(API);
        const data = await res.json();

        if (!data) return;

        updateUI(data);

    } catch (e) {
        console.log(e);
    }
}


/* UI */
function updateUI(d) {

    const set = (id, v) => {
        const el = document.getElementById(id);
        if (el) el.innerText = v;
    };

    set("signalBox", "SIGNAL : " + d.signal);
    set("trendBox", "TREND : " + d.trend);
    set("conf", "Confidence : " + d.confidence + "%");
    set("marketBox", "Market : " + d.market);
    set("riskBox", "Risk : " + d.risk);
    set("probBox", "Probability : " + d.probability + "%");
    set("strengthBox", "Strength : " + d.strength);

    const rsi = d.rsi ?? 50;
    const fill = document.getElementById("rsiFill");
    if (fill) fill.style.width = rsi + "%";

    const log = document.getElementById("historyLog");

    if (log) {
        const div = document.createElement("div");
        div.innerText =
            `${d.signal} | RSI ${rsi} | Price ${d.price}`;

        log.prepend(div);

        while (log.childNodes.length > 15) {
            log.removeChild(log.lastChild);
        }
    }
}


/* INIT */
window.onload = () => {
    fetchSignal();
    setInterval(fetchSignal, 60000);
};
