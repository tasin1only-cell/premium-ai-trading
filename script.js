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
function updateClock(){

const clock =
document.getElementById("clock");

if(clock){

clock.innerText =

new Date().toLocaleTimeString();

}

}

setInterval(updateClock,1000);

updateClock();



// ======================
// CANDLE TIMER
// ======================

let candleSec = 59;

setInterval(()=>{

candleSec--;

if(candleSec < 0){

candleSec = 59;

}

const candle =

document.getElementById(

"candle"

);

if(candle){

candle.innerText =

"Candle Ends : 00:"

+

String(candleSec)

.padStart(2,"0");

}

},1000);



// ======================
// TRADINGVIEW
// ======================

let widget = null;

function loadChart(

symbol="FX:EURUSD"

){

try{

const chart =

document.getElementById(

"tradingview_chart"

);

if(!chart) return;

chart.innerHTML = "";

widget = new TradingView.widget({

container_id:

"tradingview_chart",

width:"100%",

height:320,

symbol:symbol,

interval:"1",

theme:"dark",

style:"1",

locale:"en",

hide_side_toolbar:true,

allow_symbol_change:false

});

}

catch(err){

console.log(

"Chart Error:",

err

);

}

}



// ======================
// ASSET CHANGE
// ======================

function changeAsset(){

let asset =

document.getElementById(

"asset"

).value;


const map = {

"EUR/USD":"FX:EURUSD",

"GBP/USD":"FX:GBPUSD",

"USD/JPY":"FX:USDJPY",

"BTC/USD":"BINANCE:BTCUSDT",

"ETH/USD":"BINANCE:ETHUSDT",

"XAU/USD":"OANDA:XAUUSD"

};

loadChart(

map[asset]

||

"FX:EURUSD"

);

}



// ======================
// INIT
// ======================

window.onload = ()=>{

console.log(

"PAGE LOADED"

);

loadChart(

"FX:EURUSD"

);

};



// ======================
// AI SIGNAL
// ======================

async function generateSignal(){

console.log(

"BUTTON CLICKED"

);

try{

document.getElementById(

"signalBox"

).innerText =

"SIGNAL : LOADING...";


const res =

await fetch(

API_URL

);

if(!res.ok){

throw new Error(

"API ERROR"

);

}


const data =

await res.json();

console.log(

data

);


// =================
// TREND
// =================

const trendBox =

document.getElementById(

"trendBox"

);

trendBox.innerText =

"TREND: "

+

(data.trend

||

"--");

trendBox.style.color =

data.trend==="UP"

?

"#00ff66"

:

data.trend==="DOWN"

?

"#ff4444"

:

"gold";



// =================
// SIGNAL
// =================

document.getElementById(

"signalBox"

).innerText =

"SIGNAL : "

+

(data.signal

||

"WAIT");




// =================
// CONFIDENCE
// =================

document.getElementById(

"conf"

).innerText =

"Confidence : "

+

(data.confidence

??

"--")

+

"%";




// =================
// RSI
// =================

const rsiFill =

document.getElementById(

"rsiFill"

);

if(

rsiFill

&&

data.rsi

!==

undefined

){

rsiFill.style.width =

data.rsi

+

"%";


rsiFill.style.background =

data.rsi > 70

?

"red"

:

data.rsi < 30

?

"lime"

:

"orange";

}



// =================
// HISTORY
// =================

const log =

document.getElementById(

"historyLog"

);

if(log){

const item =

document.createElement(

"div"

);

item.innerText =

`${data.signal}

 | RSI ${data.rsi}

 | ${data.price}

 | ${new Date()

.toLocaleTimeString()}`;


log.prepend(

item

);


while(

log.childNodes.length

>

12

){

log.removeChild(

log.lastChild

);

}

}

}

catch(err){

console.log(

err

);


document.getElementById(

"signalBox"

).innerText =

"SIGNAL : ERROR";


document.getElementById(

"conf"

).innerText =

"Confidence : --";

}

}
