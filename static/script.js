let started = false;
let running = false;
let nextRun = 0;

// ======================
// GET SERVER TIME SYNC
// ======================
function getAlignedDelay() {
    const now = Date.now();
    const delay = 60000 - (now % 60000);
    return delay;
}

// ======================
// CLOCK
// ======================
setInterval(() => {
    const el = document.getElementById("clock");
    if (el) el.innerText = new Date().toLocaleTimeString();
}, 1000);

// ======================
// CANDLE TIMER (REAL SYNC FIX)
// ======================
setInterval(() => {
    const now = Date.now();
    const remaining = Math.ceil((60000 - (now % 60000)) / 1000);

    const el = document.getElementById("candle");

    if (el) {
        el.innerText = `Candle Ends : 00:${String(remaining).padStart(2, "0")}`;

        el.style.color =
            remaining <= 5 ? "red" :
            remaining <= 15 ? "orange" : "#ffcc00";
    }
}, 1000);

// ======================
// SIGNAL FETCH
// ======================
async function getSignal() {

    if (running) return;
    running = true;

    try {
        const res = await fetch("/api/signal");
        const data = await res.json();

        updateUI(data);

    } catch (e) {
        console.log(e);
    }

    running = false;
}

// ======================
// SYNC ENGINE (IMPORTANT FIX)
// ======================
function startBot() {

    if (started) return;
    started = true;

    const delay = getAlignedDelay();

    console.log("SYNC START IN:", delay / 1000, "sec");

    setTimeout(() => {

        getSignal();

        setInterval(() => {
            getSignal();
        }, 60000);

    }, delay);
}

// ======================
// INIT
// ======================
window.onload = () => {
    loadChart("FX:EURUSD");
    startBot();
};
