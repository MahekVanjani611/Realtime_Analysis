# 📈 Real-Time BTC/USDT Market Analytics Platform

A **real-time streaming analytics system** that ingests live cryptocurrency market data, processes it using **Kafka**, aggregates it into **OHLCV candles**, and visualizes it in a **live interactive dashboard using Streamlit**.

This project demonstrates **end-to-end real-time data engineering**, similar to systems used in **trading platforms, fintech analytics, and market surveillance tools**.

---

## 🚀 Features

- 🔴 Live BTC/USDT data ingestion from Binance WebSocket
- ⚡ Real-time streaming pipeline using Apache Kafka
- 📊 OHLCV (Open, High, Low, Close, Volume) aggregation
- 🕒 Time-windowed candle generation (1-minute)
- 📈 Live candlestick dashboard (auto-updating)
- 🧠 Streaming-friendly architecture (no polling DB hacks)

---

## 🏗️ System Architecture

```

Binance WebSocket
│
▼
Kafka Producer (raw_ticks)
│
▼
Kafka Topic: raw_ticks
│
▼
OHLCV Aggregator (Kafka Consumer + Producer)
│
▼
Kafka Topic: ohlcv_1m
│
▼
Streamlit Dashboard (Kafka Consumer)

```

---

## 🧰 Tech Stack

| Layer              | Technology |
|-------------------|------------|
| Data Source       | Binance WebSocket API |
| Streaming Broker  | Apache Kafka |
| Processing        | Python |
| Messaging Client  | confluent-kafka |
| Visualization     | Streamlit + Plotly |
| Containerization  | Docker + Docker Compose |

---

## 📁 Project Structure

```

project-realtime/
│
├── docker-compose.yml        # Kafka + Zookeeper setup
├── producer_ws_to_kafka.py   # WebSocket → Kafka (raw ticks)
├── ohlcv_aggregator.py       # raw_ticks → ohlcv_1m
├── dashboard.py              # Streamlit real-time dashboard
├── requirements.txt
└── README.md

````

---

## ✅ Prerequisites

Make sure you have the following installed:

- **Python 3.11.x**
- **Docker Desktop** (with WSL2 enabled on Windows)
- **pip**
- Internet connection

Verify:
```bash
python --version
docker --version
````

---

## 📦 Installation

### 1️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### `requirements.txt`

```
streamlit
pandas
plotly
confluent-kafka==2.3.0
websockets
```

Verify Kafka client:

```bash
python -c "from confluent_kafka import Consumer; print('Kafka OK')"
```

---

## 🐳 Running Kafka (Docker)

From the project root:

```bash
docker compose up -d
```

Confirm:

```bash
docker ps
```

You should see:

* `cp-kafka`
* `cp-zookeeper`

---

## ▶️ Running the Application

### Step 1: Start Binance WebSocket Producer

Streams live BTC/USDT trades into Kafka.

```bash
python producer_ws_to_kafka.py
```

Expected output:

```
Sent tick → BTCUSDT 90241.12
Sent tick → BTCUSDT 90241.35
```

---

### Step 2: Start OHLCV Aggregator

Consumes raw ticks and generates 1-minute OHLCV candles.

```bash
python ohlcv_aggregator.py
```

Expected output:

```
OHLCV: {'time': 173..., 'open': ..., 'high': ..., 'low': ..., 'close': ..., 'volume': ...}
```

---

### Step 3: Start Streamlit Dashboard

Open a **new terminal**:

```bash
python -m streamlit run dashboard.py
```

Open in browser:

```
http://localhost:8501
```

---

## 📊 Dashboard Output

* Live **candlestick chart**
* Auto-refresh every second
* Candles update as soon as Kafka publishes data
* No database polling
* True streaming behavior

⏳ First candle appears after ~1 minute.

---

## ❗ Common Issues & Fixes

### Kafka not running

```bash
docker compose down
docker compose up -d
```

### `No module named confluent_kafka`

```bash
pip install confluent-kafka==2.3.0
```

### Dashboard stuck on “Waiting for OHLCV data”

✔ Ensure both scripts are running:

* `producer_ws_to_kafka.py`
* `ohlcv_aggregator.py`

---

## 🧠 Why This Project Matters

This project demonstrates:

* Real-time data ingestion (not batch)
* Event-driven architecture
* Streaming analytics with Kafka
* Time-window aggregation
* Live dashboards without REST polling

These patterns are used in:

* Trading platforms
* Fraud detection systems
* Market surveillance
* IoT streaming analytics
* Financial data engineering roles

---

## 🔮 Future Enhancements

* RSI / MACD indicators
* Alert system (Overbought / Oversold)
* Store data in TimescaleDB
* LSTM-based trend prediction
* Multi-symbol support
* Cloud deployment (Kafka + UI split)

---

