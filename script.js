console.log("LEVEL 6B FINAL STABLE JS LOADED");

const API_URL = "https://premium-ai-trading.onrender.com/api/signal";


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

        el.style.color = remaining <= 5 ? "red" : "#ffcc00";
    }
}, 1000);


// ======================
// SAFE LOOP FLAG (IMPORTANT FIX)
// ======================
let running = false;


// ======================
// MAIN SIGNAL FUNCTION
// ======================
async function fetchSignal() {

    if (running) return;   // 🔥 prevent overlap
    running = true;

    try {

        const res = await fetch(API_URL);

        if (!res.ok) throw new Error("API ERROR");

        const data = await res.json();

        console.log("DATA:", data);

        // ======================
        // SIGNAL
        // ======================
        const signalBox = document.getElementById("signalBox");

        if (signalBox) {
            signalBox.innerText = "SIGNAL : " + data.signal;

            signalBox.style.color =
                data.signal === "BUY" ? "#00ff66" :
                data.signal === "SELL" ? "#ff4444" :
                "gold";

            signalBox.style.transform = "scale(1.15)";
            setTimeout(() => signalBox.style.transform = "scale(1)", 200);
        }

        // ======================
        // TREND
        // ======================
        const trend = document.getElementById("trendBox");

        if (trend) {
            trend.innerText = "TREND: " + data.trend;

            trend.style.color =
                data.trend === "UP" ? "#00ff66" :
                data.trend === "DOWN" ? "#ff4444" :
                "gold";
        }

        // ======================
        // CONFIDENCE
        // ======================
        const conf = document.getElementById("conf");

        if (conf) {
            conf.innerText = "Confidence : " + data.confidence + "%";

            conf.style.color =
                data.confidence > 70 ? "#00ff66" :
                data.confidence < 40 ? "#ff4444" :
                "gold";
        }

        // ======================
        // RSI BAR
        // ======================
        const rsi = document.getElementById("rsiFill");

        if (rsi) {
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
        console.log("ERROR:", err);
    }

    running = false;
}


// ======================
// AUTO RUNNER
// ======================
setInterval(fetchSignal, 5000);
fetchSignal();
