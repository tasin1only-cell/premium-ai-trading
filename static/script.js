console.log("CANDLE-LOCK AI SYSTEM LOADED");

const API_URL = "https://premium-ai-trading.onrender.com/api/signal";

let lastCandle = -1;


// ======================
// SAFE DOM HELPER
// ======================
function setText(id, value) {
    const el = document.getElementById(id);
    if (el) el.innerText = value;
}


// ======================
// CLOCK
// ======================
setInterval(() => {
    setText("clock", new Date().toLocaleTimeString());
}, 1000);


// ======================
// REAL CANDLE ID (1 MINUTE)
// ======================
function getCandleId() {
    return Math.floor(Date.now() / 60000);
}


// ======================
// CANDLE TIMER (SYNC)
// ======================
setInterval(() => {
    const sec = new Date().getSeconds();
    const remaining = 60 - sec;

    const el = document.getElementById("candle");

    if (el) {
        el.innerText = `Candle Ends : 00:${String(remaining).padStart(2, "0")}`;
        el.style.color = remaining <= 5 ? "red" : "#ffcc00";
    }
}, 1000);


// ======================
// SAFE CHART INIT
// ======================
let widget = null;

function loadChart(symbol = "FX:EURUSD") {

    try {

        const el = document.getElementById("tradingview_chart");
        if (!el) return;

        el.innerHTML = "";

        setTimeout(() => {

            if (typeof TradingView === "undefined") return;

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

        }, 500);

    } catch (e) {
        console.log("Chart Error:", e);
    }
}


// ======================
// CANDLE-LOCK SIGNAL ENGINE (IMPORTANT)
// ======================
async function fetchSignal() {

    const currentCandle = getCandleId();

    // 🔥 BLOCK MULTIPLE SIGNALS IN SAME CANDLE
    if (currentCandle === lastCandle) {
        return;
    }

    lastCandle = currentCandle;

    try {

        const res = await fetch(API_URL);
        if (!res.ok) throw new Error("API ERROR");

        const data = await res.json();

        console.log("NEW CANDLE SIGNAL:", data);

        // ======================
        // SIGNAL
        // ======================
        setText("signalBox", "SIGNAL : " + data.signal);

        const signalBox = document.getElementById("signalBox");
        if (signalBox) {
            signalBox.style.color =
                data.signal === "BUY" ? "#00ff66" :
                data.signal === "SELL" ? "#ff4444" :
                "gold";
        }

        // ======================
        // TREND
        // ======================
        setText("trendBox", "TREND: " + data.trend);

        // ======================
        // CONFIDENCE
        // ======================
        setText("conf", "Confidence : " + data.confidence + "%");

        // ======================
        // RSI
        // ======================
        const rsi = document.getElementById("rsiFill");
        if (rsi && data.rsi !== undefined) {
            rsi.style.width = data.rsi + "%";

            rsi.style.background =
                data.rsi > 70 ? "red" :
                data.rsi < 30 ? "lime" :
                "orange";
        }

        // ======================
        // HISTORY
        // ======================
        const log = document.getElementById("historyLog");

        if (log) {

            const item = document.createElement("div");

            item.style.padding = "4px";
            item.style.borderBottom = "1px solid #222";

            item.innerText =
                `${data.signal} | RSI ${data.rsi} | P ${data.price} | ${new Date().toLocaleTimeString()}`;

            log.prepend(item);

            while (log.childNodes.length > 15) {
                log.removeChild(log.lastChild);
            }
        }

    } catch (err) {
        console.log("SIGNAL ERROR:", err);
    }
}


// ======================
// AUTO LOOP (SAFE)
// ======================
setInterval(fetchSignal, 3000); // fast check, but candle lock controls output


// ======================
// INIT SYSTEM
// ======================
window.onload = () => {

    console.log("INIT CANDLE AI SYSTEM");

    loadChart("FX:EURUSD");

    fetchSignal();
};
