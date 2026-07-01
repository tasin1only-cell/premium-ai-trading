console.log("SAFE MODE JS LOADED");

const API_URL = "https://premium-ai-trading.onrender.com/api/signal";

let running = false;
let widget = null;


// ======================
// SAFE DOM HELPER
// ======================
function setText(id, value) {
    const el = document.getElementById(id);
    if (el) el.innerText = value;
}


// ======================
// CLOCK (SAFE)
// ======================
setInterval(() => {
    try {
        setText("clock", new Date().toLocaleTimeString());
    } catch (e) {
        console.log(e);
    }
}, 1000);


// ======================
// CANDLE TIMER (SAFE)
// ======================
setInterval(() => {
    try {
        const sec = new Date().getSeconds();
        const remaining = 60 - sec;

        const el = document.getElementById("candle");
        if (el) {
            el.innerText = `Candle Ends : 00:${String(remaining).padStart(2, "0")}`;
            el.style.color = remaining <= 5 ? "red" : "#ffcc00";
        }
    } catch (e) {
        console.log(e);
    }
}, 1000);


// ======================
// CHART SAFE INIT
// ======================
function loadChart(symbol = "FX:EURUSD") {

    try {

        const el = document.getElementById("tradingview_chart");
        if (!el) return;

        el.innerHTML = "";

        setTimeout(() => {

            if (typeof TradingView === "undefined") {
                console.log("TradingView not loaded");
                return;
            }

            widget = new TradingView.widget({
                container_id: "tradingview_chart",
                width: "100%",
                height: 320,
                symbol: symbol,
                interval: "1",
                theme: "dark",
                style: "1",
                locale: "en",
                hide_side_toolbar: true,
                allow_symbol_change: false
            });

        }, 600);

    } catch (e) {
        console.log("Chart Error:", e);
    }
}


// ======================
// SAFE SIGNAL ENGINE
// ======================
async function fetchSignal() {

    if (running) return;
    running = true;

    try {

        const res = await fetch(API_URL);

        if (!res.ok) throw new Error("API ERROR");

        const data = await res.json();

        console.log("DATA:", data);

        setText("signalBox", "SIGNAL : " + data.signal);
        setText("trendBox", "TREND: " + data.trend);
        setText("conf", "Confidence : " + data.confidence + "%");

        const rsi = document.getElementById("rsiFill");
        if (rsi && data.rsi) {
            rsi.style.width = data.rsi + "%";
        }

        const log = document.getElementById("historyLog");

        if (log) {
            const item = document.createElement("div");
            item.innerText =
                `${data.signal} | RSI ${data.rsi} | ${data.price}`;

            log.prepend(item);

            while (log.childNodes.length > 10) {
                log.removeChild(log.lastChild);
            }
        }

    } catch (err) {
        console.log("SIGNAL ERROR:", err);

        setText("signalBox", "SIGNAL : ERROR");
    }

    running = false;
}


// ======================
// AUTO RUN SAFE
// ======================
setInterval(() => {
    fetchSignal();
}, 5000);


// ======================
// INIT SAFE
// ======================
window.onload = () => {

    console.log("INIT SAFE SYSTEM");

    try {
        loadChart("FX:EURUSD");
    } catch (e) {
        console.log("INIT ERROR:", e);
    }

    fetchSignal();
};
