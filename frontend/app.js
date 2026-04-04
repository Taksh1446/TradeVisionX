const API = "http://localhost:5000";

function login() {
    fetch(API + "/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            email: document.getElementById("email").value,
            password: document.getElementById("password").value
        })
    })
    .then(res => res.json())
    .then(data => {
        localStorage.setItem("token", data.token);
        window.location = "dashboard.html";
    });
}

function buyStock() {
    fetch(API + "/buy", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            user_id: 1,
            symbol: document.getElementById("symbol").value,
            qty: document.getElementById("qty").value
        })
    })
    .then(res => res.json())
    .then(data => alert(data.message));
}