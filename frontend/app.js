const API = "https://tradevision-backend-1dva.onrender.com";

// ------------------ PROFILE ------------------
function loadProfile() {
    const token = localStorage.getItem("token");

    fetch(API + "/profile", {
        headers: { "Authorization": token }
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("username").innerText = data.name;
        document.getElementById("balance").innerText = data.balance;
    });
}

// ------------------ GET PRICE (LIVE) ------------------
function getPrice() {
    const symbol = document.getElementById("search").value;

    fetch(`https://query1.finance.yahoo.com/v7/finance/quote?symbols=${symbol}`)
    .then(res => res.json())
    .then(data => {
        const price = data.quoteResponse.result[0].regularMarketPrice;
        document.getElementById("price").innerText = "Price: $" + price;

        // store for trading
        window.currentPrice = price;
    });
}

// ------------------ BUY ------------------
function buyStock() {
    const token = localStorage.getItem("token");

    fetch(API + "/buy", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": token
        },
        body: JSON.stringify({
            user_id: 1,
            symbol: document.getElementById("symbol").value,
            quantity: document.getElementById("qty").value,
            price: window.currentPrice || 100
        })
    })
    .then(res => res.json())
    .then(data => alert(data.message));
}

// ------------------ SELL ------------------
function sellStock() {
    const token = localStorage.getItem("token");

    fetch(API + "/sell", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": token
        },
        body: JSON.stringify({
            user_id: 1,
            symbol: document.getElementById("symbol").value,
            quantity: document.getElementById("qty").value,
            price: window.currentPrice || 100
        })
    })
    .then(res => res.json())
    .then(data => alert(data.message));
}

// ------------------ LOGOUT ------------------
function logout() {
    localStorage.removeItem("token");
    window.location = "index.html";
}
