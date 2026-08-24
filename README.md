# 📈 TradeVisionX

**A full-stack, distributed trading simulation platform with real-time market data, secure authentication, and ML-powered stock predictions.**

![Status](https://img.shields.io/badge/status-active-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![Next.js](https://img.shields.io/badge/frontend-Next.js%20%2B%20React-black)
![Flask](https://img.shields.io/badge/backend-Flask-lightgrey)
![PostgreSQL](https://img.shields.io/badge/database-PostgreSQL-336791)
![JWT](https://img.shields.io/badge/auth-JWT-orange)

---

## 🧭 Overview

TradeVisionX is a **multi-service, full-stack trading simulator** built to mirror the architecture of a real brokerage platform. Users sign up with a virtual wallet, trade simulated stocks in a live-updating market, track portfolio performance, and get **ML-powered trend predictions** for any ticker.

The project was built to explore real-world backend engineering problems — concurrency-safe money transfers, stateless authentication, and real-time data propagation — rather than just building another CRUD app.

---

## ✨ Features

- 🔐 **Secure Authentication** — Stateless JWT-based auth with bcrypt password hashing
- 💰 **Virtual Wallet & Portfolio** — Track wallet balance, holdings, invested capital, and returns
- 📊 **Live Market Data** — Simulated real-time price feed with candlestick charts (1m/30m/1h/1D)
- ⚡ **Concurrency-Safe Trading** — Row-level locking (`SELECT FOR UPDATE`) on wallet/portfolio rows to prevent race conditions on simultaneous buy/sell requests
- 🤖 **AI Analysis** — Linear regression–based trend prediction with bullish/bearish signal, profit probability, volatility, risk score, and 1/5/10-day price targets
- 📈 **Performance Analytics** — Win rate, win/loss ratio, total P&L, net returns, and trade history
- 🧱 **Clean Layered Architecture** — Separated data, service, and route layers on the backend

---

## 🖼️ Screenshots

### 🔑 Sign In
Secure login screen with JWT-based session handling.


<img width="2878" height="1512" alt="Screenshot 2026-08-24 203847" src="https://github.com/user-attachments/assets/51134666-0812-4ae2-87ea-ed2071621f2b" />



### 🏠 Dashboard
Wallet balance, portfolio value, P&L, recent trades, and performance overview at a glance.

<img width="2808" height="1564" alt="Screenshot 2026-08-24 203901" src="https://github.com/user-attachments/assets/2bef2d07-9984-44f7-92f2-0967adfff914" />


### 💹 Live Market
Real-time candlestick charts with buy/sell execution panel.

<img width="2808" height="1500" alt="Screenshot 2026-08-24 203927" src="https://github.com/user-attachments/assets/a15a85ef-b74c-4215-aa8a-db70b96187fd" />


### 🤖 AI Analysis
ML-powered price prediction with trend, risk score, and price targets.
<img width="2878" height="1500" alt="Screenshot 2026-08-24 203945" src="https://github.com/user-attachments/assets/a4c6c284-33ca-47cd-a49e-ccd9b04b5183" />


---

## 🏗️ Tech Stack

| Layer            | Technology                                              |
|-------------------|----------------------------------------------------------|
| Frontend          | Next.js, React.js                                        |
| Backend           | Flask (Python), REST API                                 |
| Database          | PostgreSQL (local instance, normalized relational schema) |
| Authentication    | JWT (stateless) + bcrypt password hashing                |
| Real-time layer   | Polling-based market data pipeline (producer–consumer)   |
| Concurrency       | Row-level locking (`SELECT FOR UPDATE`) for trade safety |

**Architecture at a glance:**

```
┌──────────────┐        REST API (JWT-authenticated)        ┌──────────────┐
│   Next.js /   │ ───────────────────────────────────────▶ │    Flask      │
│  React Client │ ◀─────────────────────────────────────── │  REST API     │
└──────────────┘                                            └──────┬───────┘
                                                                     │
                                                          Row-level  │  locking
                                                                     ▼
                                                            ┌──────────────┐
                                                            │  PostgreSQL   │
                                                            │ users/trades/ │
                                                            │  portfolio    │
                                                            └──────────────┘
```

---

## 🚀 Getting Started

### Prerequisites

- Node.js (v18+)
- Python (v3.10+)
- PostgreSQL (running locally)

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd tradevisionx
```

### 2. Backend setup (Flask)

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in `/backend`:

```env
DATABASE_URL=postgresql://<user>:<password>@localhost:5432/tradevisionx
JWT_SECRET_KEY=<your-secret-key>
FLASK_ENV=development
```

Run database migrations, then start the server:

```bash
flask db upgrade
flask run
```

### 3. Frontend setup (Next.js)

```bash
cd frontend
npm install
```

Create a `.env.local` file in `/frontend`:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:5000
```

```bash
npm run dev
```

App will be live at `http://localhost:3000`.

---

## 🔐 Authentication Flow

1. User registers/logs in → password verified against bcrypt hash
2. Server issues a stateless **JWT** on successful login
3. Client attaches the JWT to every subsequent API request
4. Protected routes validate the token before executing trade/portfolio logic

---

## 💱 Trade Execution Flow

1. User submits a buy/sell request from the Market page
2. Backend locks the relevant wallet & portfolio rows (`SELECT FOR UPDATE`)
3. Trade is validated (sufficient balance/holdings) and executed atomically
4. Wallet, portfolio, and trade history are updated in the same transaction
5. Lock is released — safe even under simultaneous requests on the same account

---

## 🤖 AI Analysis Module

- Uses **linear regression** over 30-day historical price data to project short-term trends
- Outputs: trend direction (Bullish/Bearish), risk level, profit probability, volatility, 10-day momentum, and model R²
- Generates 1-day, 5-day, and 10-day price targets for the selected ticker

---

## 📂 Project Structure

```
tradevisionx/
├── frontend/              # Next.js + React client
│   ├── pages/
│   ├── components/
│   └── ...
├── backend/                # Flask REST API
│   ├── routes/
│   ├── services/
│   ├── models/
│   └── ...
├── screenshots/            # README screenshots
└── README.md
```

---

## 🛣️ Roadmap

- [ ] Migrate real-time price feed from polling to WebSockets
- [ ] Add order types (limit/stop-loss)
- [ ] Expand AI Analysis with additional model comparisons
- [ ] Dockerize backend + database for one-command setup

---

## 👤 Author

**Taksh Patel**
B.Tech ICT, Pandit Deendayal Energy University (Class of 2028)

- LinkedIn: `www.linkedin.com/in/taksh-samirkumar-patel-6a6b97325`
- GitHub: `https://github.com/Taksh1446`
- LeetCode: `https://leetcode.com/u/5EWSbJZA6M/`

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](./LICENSE) file for details.
