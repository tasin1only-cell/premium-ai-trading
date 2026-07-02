console.log("LEVEL 7 STABLE AI LOADED");

const API_URL = "/api/signal";

let running = false;
let lastSignal = "";


/* ================= CLOCK ================= */

setInterval(() => {

    const el = document.getElementById("clock");

    if (el) {

        el.innerText = new Date().toLocaleTimeString();

    }

}, 1000);



/* ================= CANDLE TIMER ================= */

setInterval(() => {

    const el = document.getElementById("candle");

    if (!el) return;

    const sec = new Date().getSeconds();

    const remaining = 60 - sec;

    el.innerText =
        `Candle Ends : 00:${String(remaining).padStart(2, "0")}`;

}, 1000);



/* ================= CHART ================= */

function loadChart(symbol = "BINANCE:BTCUSDT") {

    const el = document.getElementById("tradingview_chart");

    if (!el) return;

    el.innerHTML = "";

    if (typeof TradingView === "undefined") {

        setTimeout(() => {

            loadChart(symbol);

        }, 1000);

        return;

    }

    new TradingView.widget({

        container_id: "tradingview_chart",

        width: "100%",

        height: 320,

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



/* ================= ASSET ================= */

function changeAsset() {

    const asset =

        document.getElementById("asset").value;

    const map = {

        "EUR/USD": "FX:EURUSD",

        "GBP/USD": "FX:GBPUSD",

        "USD/JPY": "FX:USDJPY",

        "BTC/USD": "BINANCE:BTCUSDT",

        "ETH/USD": "BINANCE:ETHUSDT",

        "XAU/USD": "OANDA:XAUUSD"

    };

    loadChart(

        map[asset]

    );

}



/* ================= UI ================= */

function set(id, val) {

    const el = document.getElementById(id);

    if (el) {

        el.innerText = val;

    }

}



function updateUI(d) {

    set(

        "signalBox",

        "SIGNAL : " + d.signal

    );

    set(

        "trendBox",

        "TREND : " + d.trend

    );

    set(

        "conf",

        "Confidence : " +

        d.confidence +

        "%"

    );

    set(

        "marketBox",

        "Market : " +

        d.market

    );

    set(

        "riskBox",

        "Risk : " +

        d.risk

    );

    set(

        "probBox",

        "Probability : " +

        d.probability +

        "%"

    );

    set(

        "strengthBox",

        "Strength : " +

        d.strength

    );



    const fill =

        document.getElementById(

            "rsiFill"

        );

    if (fill) {

        fill.style.width =

            d.rsi + "%";

    }



    const log =

        document.getElementById(

            "historyLog"

        );



    if (log) {

        const current =

            `${d.signal}_${d.price}`;



        if (

            current !== lastSignal

        ) {

            lastSignal = current;

            const div =

                document.createElement(

                    "div"

                );



            div.innerText =

                `${d.signal} | RSI ${d.rsi} | Price ${d.price}`;



            log.prepend(div);



            while (

                log.childNodes.length >

                15

            ) {

                log.removeChild(

                    log.lastChild

                );

            }

        }

    }

}



/* ================= API ================= */

async function getSignal() {

    if (running) return;

    running = true;

    try {

        const res =

            await fetch(

                API_URL +

                "?t=" +

                Date.now()

            );



        const data =

            await res.json();



        updateUI(

            data

        );



    } catch (e) {

        console.log(

            "API ERROR",

            e

        );

    }



    setTimeout(

        () => {

            running = false;

        },

        1000

    );

}



/* ================= BOT ================= */

function startBot() {

    getSignal();

    setInterval(

        getSignal,

        5000

    );

}



/* ================= INIT ================= */

window.onload = () => {

    loadChart(

        "BINANCE:BTCUSDT"

    );



    startBot();

};
