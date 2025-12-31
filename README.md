# Real-Time BTC/USDT Analytics Platform

## Architecture
Binance WebSocket → Kafka → Streamlit Dashboard

## Features
- Real-time OHLCV candles
- RSI & MACD indicators
- Volume analysis
- Alerting (Overbought / Oversold)
- Kafka-based streaming pipeline

## Why Kafka?
- Decouples ingestion and analytics
- Fault tolerant
- Scalable to multiple consumers

## Tech Stack
Python, Kafka, Streamlit, Plotly
