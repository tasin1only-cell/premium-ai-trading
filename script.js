
// ======================
// DEBUG
// ======================
console.log("SCRIPT LOADED");

// ======================
// API
// ======================
const API_URL =
"https://premium-ai-trading.onrender.com/api/signal";


// ======================
// CLOCK
// ======================
setInterval(()=>{
document.getElementById("clock").innerText =
new Date().toLocaleTimeString();
},1000);


// ======================
// CANDLE TIMER
// ======================
let candleSec = 59;

setInterval(()=>{

candleSec--;

if(candleSec < 0) candleSec = 59;

const c = document.getElementById("candle");

if(c){
c.innerText = "Candle Ends : 00:" +
String(candleSec).padStart(2,"0");
}

},1000);


// ======================
// SAFE SIGNAL FUNCTION
// ======================
async function generateSignal(){

try{

document.getElementById("signalBox").innerText =
"SIGNAL : ANALYZING...";

document.getElementById("conf").innerText =
"Confidence : ...";

const res = await fetch(API_URL);

if(!res.ok){
throw new Error("API ERROR " + res.status);
}

const data = await res.json();

console.log("API DATA:", data);

// ======================
// SAFE FALLBACK (IMPORTANT)
// ======================

const signal = data.signal || "WAIT";
const confidence = data.confidence ?? 55;
const rsi = data.rsi ?? 50;
const trend = data.trend || "SIDE";
const price = data.price || 0;


// ======================
// TREND UI
// ======================
const trendBox =
document.getElementById("trendBox");

trendBox.innerText =
"TREND: " + trend;

trendBox.style.color =
trend === "UP"
? "lime"
: trend === "DOWN"
? "red"
: "gold";


// ======================
// SIGNAL UI
// ======================
document.getElementById("signalBox").innerText =
"SIGNAL : " + signal;


// ======================
// CONFIDENCE UI (NO ZERO ISSUE)
// ======================
document.getElementById("conf").innerText =
"Confidence : " + confidence + "%";


// ======================
// RSI BAR
// ======================
const rsiFill =
document.getElementById("rsiFill");

if(rsiFill){

rsiFill.style.width = rsi + "%";

rsiFill.style.background =
rsi > 70 ? "red" :
rsi < 30 ? "lime" :
"orange";

}


// ======================
// HISTORY
// ======================
const log =
document.getElementById("historyLog");

if(log){

const item =
document.createElement("div");

item.innerText =
`${signal} | RSI ${rsi} | ${price} | ${new Date().toLocaleTimeString()}`;

log.prepend(item);

if(log.childNodes.length > 12){
log.removeChild(log.lastChild);
}

}

}

catch(err){

console.log("ERROR:", err);

document.getElementById("signalBox").innerText =
"SIGNAL : ERROR";

document.getElementById("conf").innerText =
"Confidence : 50%";

}

}
