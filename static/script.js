console.log("LEVEL 7 AI TRADING JS LOADED");

const API_URL = "/api/signal";
const CANDLE_URL = "/api/candles";

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
// CANDLE TIMER
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
// UI UPDATE
// ======================
function updateUI(data) {

    const signalBox = document.getElementById("signalBox");
    const trendBox = document.getElementById("trendBox");
    const conf = document.getElementById("conf");
    const rsiFill = document.getElementById("rsiFill");
    const log = document.getElementById("historyLog");

    const rsi = data.rsi ?? 50;
    const price = data.price ?? 0;

    if (signalBox) signalBox.innerText = "SIGNAL : " + data.signal;
    if (trendBox) trendBox.innerText = "TREND : " + data.trend;
    if (conf) conf.innerText = "Confidence : " + data.confidence + "%";

    if (rsiFill) rsiFill.style.width = rsi + "%";

    if (log) {
        const item = document.createElement("div");
        item.innerText = `${data.signal} | RSI ${rsi} | Price ${price}`;
        log.prepend(item);

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

    } catch (err) {
        console.log(err);
    }

    setTimeout(() => {
        running = false;
    }, 1000);
}


// ======================
// START
// ======================
function startBot() {

    if (started) return;
    started = true;

    generateSignal();
    setInterval(generateSignal, 60000);
}


// ======================
window.onload = () => {
    startBot();
};
