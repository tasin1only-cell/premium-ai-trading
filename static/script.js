console.log("LEVEL 7 STABLE AI LOADED");

const API_URL = "/api/signal";

let running = false;


setInterval(() => {
    const el = document.getElementById("clock");
    if (el) el.innerText = new Date().toLocaleTimeString();
}, 1000);


setInterval(() => {
    const el = document.getElementById("candle");
    if (!el) return;

    const sec = new Date().getSeconds();
    const remaining = 60 - sec;

    el.innerText = `Candle Ends : 00:${String(remaining).padStart(2,"0")}`;
}, 1000);


function set(id, val) {
    const el = document.getElementById(id);
    if (el) el.innerText = val;
}


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


async function getSignal() {
    if (running) return;
    running = true;

    try {
        const res = await fetch(API_URL + "?t=" + Date.now());
        const data = await res.json();
        updateUI(data);
    } catch (e) {
        console.log("API ERROR", e);
    }

    setTimeout(() => running = false, 1200);
}


function startBot() {
    getSignal();
    setInterval(getSignal, 4000);
}


window.onload = () => {
    startBot();
};
