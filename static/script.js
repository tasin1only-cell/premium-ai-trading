console.log("AI TRADING PRO FULL FIX LOADED");

const API_URL = "/api/signal";

let running = false;
let lastSignalTime = 0;

// ================= CLOCK =================
setInterval(() => {
    const el = document.getElementById("clock");
    if (el) el.innerText = new Date().toLocaleTimeString();
}, 1000);

// ================= CANDLE TIMER =================
setInterval(() => {
    const el = document.getElementById("candle");
    if (!el) return;

    const sec = new Date().getSeconds();
    const remaining = 60 - sec;

    el.innerText = `Candle Ends : 00:${String(remaining).padStart(2,"0")}`;
}, 1000);

// ================= UI SET =================
function set(id, val){
    const el = document.getElementById(id);
    if (el) el.innerText = val;
}

// ================= UPDATE UI =================
function updateUI(d){

    set("signalBox", "SIGNAL : " + d.signal);
    set("trendBox", "TREND : " + d.trend);
    set("conf", "Confidence : " + d.confidence + "%");
    set("marketBox", "Market : " + d.market);
    set("riskBox", "Risk : " + d.risk);
    set("probBox", "Probability : " + d.probability + "%");
    set("strengthBox", "Strength : " + d.strength);

    const rsiFill = document.getElementById("rsiFill");
    if (rsiFill) rsiFill.style.width = d.rsi + "%";

    // history fix (no spam)
    const now = Date.now();
    if (now - lastSignalTime > 55000) {
        lastSignalTime = now;

        const log = document.getElementById("historyLog");
        if (log) {
            const div = document.createElement("div");
            div.innerText = `${d.signal} | RSI ${d.rsi} | Price ${d.price}`;
            log.prepend(div);
        }
    }
}

// ================= SIGNAL API =================
async function getSignal(){
    if (running) return;
    running = true;

    try{
        const res = await fetch(API_URL + "?t=" + Date.now());
        const data = await res.json();
        updateUI(data);
    }catch(e){
        console.log("API ERROR", e);
    }

    setTimeout(()=> running = false, 800);
}

// ================= CHART FIX (IMPORTANT) =================
function loadChart(symbol="FX:EURUSD"){

    const el = document.getElementById("tradingview_chart");
    if(!el) return;

    el.innerHTML = "";

    // wait until TV loads
    if(typeof TradingView === "undefined"){
        setTimeout(()=> loadChart(symbol), 1000);
        return;
    }

    new TradingView.widget({
        container_id: "tradingview_chart",
        width: "100%",
        height: 350,
        symbol: symbol,
        interval: "1",
        theme: "dark",
        style: "1",
        locale: "en",
        autosize: true,
        hide_side_toolbar: true,
        allow_symbol_change: false
    });
}

// ================= ASSET =================
function changeAsset(){
    const asset = document.getElementById("asset").value;

    const map = {
        "EUR/USD":"FX:EURUSD",
        "GBP/USD":"FX:GBPUSD",
        "USD/JPY":"FX:USDJPY",
        "BTC/USD":"BINANCE:BTCUSDT",
        "ETH/USD":"BINANCE:ETHUSDT",
        "XAU/USD":"OANDA:XAUUSD"
    };

    loadChart(map[asset]);
}

// ================= START =================
function startBot(){
    getSignal();
    setInterval(getSignal, 2000);
}

// ================= INIT (IMPORTANT FIX) =================
window.onload = () => {

    // chart must load AFTER DOM ready
    setTimeout(() => {
        loadChart("FX:EURUSD");
    }, 1500);

    startBot();
};
