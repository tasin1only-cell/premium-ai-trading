
const assets = [
"EUR/USD", "GBP/USD", "USD/JPY",
"AUD/USD", "USD/CHF", "USD/CAD",
"NZD/USD", "EUR/GBP", "EUR/JPY",
"GBP/JPY", "BTC/USD", "ETH/USD",
"XAU/USD (Gold)", "XAG/USD (Silver)"
];

const sessions = ["Global", "USA Session", "London Session", "Asia Session"];

// AUTO BASE URL (fix IP issues)
function getBaseURL() {
    return "http://192.168.0.100:5000";
}

async function generateSignal() {

    let asset = document.getElementById("asset").value;
    let session = document.getElementById("country").value;

    let url = getBaseURL() + "/predict";

    console.log("Sending request to:", url);

    try {

        let response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                rsi: Math.floor(Math.random() * 100),
                macd: Math.random() > 0.5 ? "BUY" : "SELL",
                ema: Math.random() > 0.5 ? "UP" : "DOWN"
            })
        });

        if (!response.ok) {
            throw new Error("HTTP Error: " + response.status);
        }

        let data = await response.json();

        console.log("Response from server:", data);

        document.getElementById("signalBox").innerText =
            "SIGNAL: " + (data.signal || "NO DATA");

        document.getElementById("conf").innerText =
            "CONFIDENCE: " + (data.confidence || 0) + "%";

        document.getElementById("extra").innerText =
            "Asset: " + asset + " | Session: " + session;

    } catch (error) {

        console.log("ERROR:", error);

        document.getElementById("signalBox").innerText =
            "SIGNAL: ERROR";

        document.getElementById("conf").innerText =
            "CONFIDENCE: 0%";

        document.getElementById("extra").innerText =
            "Backend not connected ❌ Check Flask / IP / WiFi";
    }
}