console.log("LEVEL 9 STABLE SYSTEM LOADED");

const API_URL = "/api/signal";

let running = false;
let started = false;
let lastMinute = -1;

/* CLOCK */
setInterval(() => {
    const el = document.getElementById("clock");
    if (el) el.innerText = new Date().toLocaleTimeString();
}, 1000);

/* CANDLE SYNC (REAL 1 MIN FIX) */
function getMinute(){
    return new Date().getMinutes();
}

setInterval(() => {

    const nowMin = getMinute();

    // ONLY NEW CANDLE SIGNAL
    if(nowMin !== lastMinute){
        lastMinute = nowMin;
        generateSignal();
    }

    // candle timer UI
    const sec = new Date().getSeconds();
    const remaining = 60 - sec;

    const el = document.getElementById("candle");
    if(el){
        el.innerText = `Candle Ends : 00:${String(remaining).padStart(2,"0")}`;
    }

}, 1000);


/* CHART SAFE LOAD */
function loadChart(symbol="FX:EURUSD"){

    setTimeout(() => {

        const el = document.getElementById("tradingview_chart");
        if(!el) return;

        el.innerHTML = "";

        if(!window.TradingView) return;

        new TradingView.widget({
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
}


/* UI UPDATE (SAFE + COLOR FIX) */
function updateUI(data){

    if(!data) return;

    const set = (id,val)=>{
        const el = document.getElementById(id);
        if(el) el.innerText = val;
    };

    set("signalBox","SIGNAL : " + (data.signal || "WAIT"));
    set("trendBox","TREND : " + (data.trend || "SIDE"));
    set("conf","Confidence : " + (data.confidence ?? 50) + "%");
    set("marketBox","Market : " + (data.market || "UNKNOWN"));
    set("riskBox","Risk : " + (data.risk || "LOW"));
    set("probBox","Probability : " + (data.probability ?? 0) + "%");
    set("strengthBox","Strength : " + (data.strength || "NONE"));

    const rsi = data.rsi ?? 50;
    const fill = document.getElementById("rsiFill");
    if(fill) fill.style.width = rsi + "%";

    const log = document.getElementById("historyLog");

    if(log){
        const div = document.createElement("div");
        div.innerText =
        `${data.signal} | RSI ${rsi.toFixed(2)} | Price ${data.price} | Prob ${data.probability ?? 0}%`;

        log.prepend(div);

        while(log.childNodes.length > 15){
            log.removeChild(log.lastChild);
        }
    }
}


/* SIGNAL */
async function generateSignal(){

    if(running) return;
    running = true;

    try{
        const res = await fetch(API_URL);
        const data = await res.json();

        // SAFE GUARD (IMPORTANT)
        if(!data || !data.price){
            running = false;
            return;
        }

        updateUI(data);

    }catch(e){
        console.log("API ERROR",e);
    }

    setTimeout(()=>running=false,1200);
}


/* INIT */
window.onload = ()=>{

    loadChart();
    generateSignal();

    // backup refresh (NO spam)
    setInterval(generateSignal, 15000);
};
