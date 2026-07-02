console.log("AI TRADING PRO V4 FIXED LOADED");

const API_URL = "/api/signal";

let lastSignalTime = 0;
let lastSignal = "";
let running = false;


/* ================= CLOCK ================= */
setInterval(() => {
    const el = document.getElementById("clock");
    if (el) el.innerText = new Date().toLocaleTimeString();
}, 1000);


/* ================= CANDLE TIMER ================= */
setInterval(() => {
    const el = document.getElementById("candle");
    if (!el) return;

    const sec = new Date().getSeconds();
    const remaining = 60 - sec;

    el.innerText = `Candle Ends : 00:${String(remaining).padStart(2,"0")}`;
}, 1000);


/* ================= HELPERS ================= */
function set(id, val) {
    const el = document.getElementById(id);
    if (el) el.innerText = val;
}


/* ================= UI UPDATE ================= */
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

    // ================= SIGNAL HISTORY (CANDLE BASED) =================
    const now = Date.now();

    if (now - lastSignalTime > 55000) {
        lastSignalTime = now;

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

    lastSignal = d.signal;
}


/* ================= API CALL ================= */
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

    setTimeout(() => running = false, 800);
}


/* ================= BOT LOOP (FAST UPDATE) ================= */
function startBot() {
    getSignal();
    setInterval(getSignal, 2000);   // 🔥 FAST SIGNAL UPDATE
}


/* ================= INIT ================= */
window.onload = () => {
    startBot();
};
