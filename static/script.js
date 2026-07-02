console.log("FINAL STABLE AI SYSTEM LOADED");

const API_URL = "/api/signal";

let running = false;
let lastMinute = new Date().getMinutes();

/* CLOCK */
setInterval(() => {
    const el = document.getElementById("clock");
    if (el) el.innerText = new Date().toLocaleTimeString();
}, 1000);

/* CANDLE SYNC */
setInterval(() => {
    const now = new Date();
    const minute = now.getMinutes();
    const sec = now.getSeconds();

    const el = document.getElementById("candle");

    if (el) {
        el.innerText = `Candle Ends : 00:${String(60 - sec).padStart(2,"0")}`;
    }

    if (minute !== lastMinute) {
        lastMinute = minute;
        generateSignal();
    }

}, 1000);

/* SAFE FETCH */
async function generateSignal() {

    if (running) return;
    running = true;

    try {
        const res = await fetch(API_URL);
        const data = await res.json();

        if (!data) return;

        updateUI(data);

    } catch (e) {
        console.log("API ERROR", e);
    }

    setTimeout(() => running = false, 800);
}

/* UI */
function updateUI(data) {

    const set = (id, val) => {
        const el = document.getElementById(id);
        if (el) el.innerText = val;
    };

    set("signalBox", "SIGNAL : " + (data.signal || "WAIT"));
    set("trendBox", "TREND : " + (data.trend || "SIDE"));
    set("conf", "Confidence : " + (data.confidence || 50) + "%");
    set("marketBox", "Market : " + (data.market || "UNKNOWN"));
    set("riskBox", "Risk : " + (data.risk || "LOW"));
    set("probBox", "Probability : " + (data.probability || 0) + "%");
    set("strengthBox", "Strength : " + (data.strength || "NONE"));

    const rsi = data.rsi ?? 50;
    const fill = document.getElementById("rsiFill");
    if (fill) fill.style.width = rsi + "%";

    const log = document.getElementById("historyLog");

    if (log) {
        const div = document.createElement("div");
        div.innerText =
            `${data.signal} | RSI ${rsi} | Price ${data.price} | Prob ${data.probability}%`;

        log.prepend(div);

        while (log.childNodes.length > 15) {
            log.removeChild(log.lastChild);
        }
    }
}

/* INIT */
window.onload = () => {
    generateSignal();
    setInterval(generateSignal, 10000);
};
