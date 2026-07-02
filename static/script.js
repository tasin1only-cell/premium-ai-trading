console.log("LEVEL 9 STABLE SYSTEM LOADED");

const API_URL = "/api/signal";

let running = false;
let started = false;

// CLOCK
setInterval(() => {
    const el = document.getElementById("clock");
    if (el) el.innerText = new Date().toLocaleTimeString();
}, 1000);

// CANDLE SYNC
function getRemainingMs() {
    const now = new Date();
    return (60 - now.getSeconds()) * 1000 - now.getMilliseconds();
}

// SIGNAL SYNC ENGINE
function scheduleSignal() {
    const delay = getRemainingMs();

    setTimeout(async () => {
        await fetchSignal();
        scheduleSignal();
    }, delay);
}

// FETCH SIGNAL
async function fetchSignal() {
    if (running) return;
    running = true;

    try {
        const res = await fetch(API_URL + "?t=" + Date.now());
        const data = await res.json();
        updateUI(data);
    } catch (e) {
        console.log(e);
    }

    setTimeout(() => running = false, 800);
}

// UI
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

    const fill = document.getElementById("rsiFill");
    if (fill) fill.style.width = (data.rsi || 50) + "%";

    const log = document.getElementById("historyLog");

    if (log) {
        const div = document.createElement("div");
        div.innerText = `${data.signal} | RSI ${data.rsi} | ${data.price}`;
        log.prepend(div);
    }
}

// START
function startBot() {
    if (started) return;
    started = true;

    fetchSignal();
    scheduleSignal();
}

window.onload = startBot;
