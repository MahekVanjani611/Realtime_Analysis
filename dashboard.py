# # import streamlit as st
# # import websocket, json, time
# # import pandas as pd
# # from collections import deque
# # import plotly.graph_objects as go
# # import threading

# # st.set_page_config(layout="wide")
# # st.title("📈 Real-Time BTC/USDT Dashboard")

# # WS_URL = "ws://127.0.0.1:8000/ws/live"
# # data = deque(maxlen=200)

# # def on_message(ws, msg):
# #     d = json.loads(msg)
# #     data.append({
# #         "time": pd.to_datetime(d["time"], unit="ms"),
# #         "open": d["open"],
# #         "high": d["high"],
# #         "low": d["low"],
# #         "close": d["close"],
# #         "volume": d["volume"]
# #     })

# # def start_ws():
# #     ws = websocket.WebSocketApp(WS_URL, on_message=on_message)
# #     ws.run_forever()

# # threading.Thread(target=start_ws, daemon=True).start()

# # price = st.empty()
# # chart = st.empty()

# # while True:
# #     if len(data) > 10:
# #         df = pd.DataFrame(data)

# #         price.metric("BTC Price", f"{df.iloc[-1]['close']:.2f}")

# #         fig = go.Figure(go.Candlestick(
# #             x=df["time"],
# #             open=df["open"],
# #             high=df["high"],
# #             low=df["low"],
# #             close=df["close"]
# #         ))

# #         fig.update_layout(
# #             xaxis_rangeslider_visible=False,
# #             template="plotly_dark",
# #             height=500
# #         )

# #         chart.plotly_chart(fig, use_container_width=True)

# #     time.sleep(1)


# import streamlit as st
# from confluent_kafka import Consumer
# import json
# import pandas as pd
# import time

# st.set_page_config(page_title="BTC/USDT Live Dashboard", layout="wide")

# st.title("📈 BTC/USDT – Real-Time OHLCV")

# # ---------------- Kafka Consumer ----------------
# consumer = Consumer({
#     "bootstrap.servers": "localhost:9092",
#     "group.id": "streamlit-dashboard",
#     "auto.offset.reset": "latest"
# })

# consumer.subscribe(["ohlcv_1m"])

# # ---------------- State ----------------
# if "data" not in st.session_state:
#     st.session_state.data = []

# placeholder = st.empty()

# # ---------------- Main Loop ----------------
# while True:
#     msg = consumer.poll(1.0)

#     if msg is not None and not msg.error():
#         candle = json.loads(msg.value().decode("utf-8"))
#         st.session_state.data.append(candle)

#         # keep last 200 candles
#         st.session_state.data = st.session_state.data[-200:]

#         df = pd.DataFrame(st.session_state.data)
#         df["time"] = pd.to_datetime(df["time"], unit="ms")

#         with placeholder.container():
#             st.subheader("OHLCV (1m)")
#             st.dataframe(df.tail(5), use_container_width=True)

#             st.subheader("Close Price")
#             st.line_chart(df.set_index("time")["close"])

#     time.sleep(1)

# import streamlit as st
# from confluent_kafka import Consumer
# import json
# import pandas as pd
# import time
# import plotly.graph_objects as go

# def compute_rsi(series, period=14):
#     delta = series.diff()
#     gain = delta.clip(lower=0)
#     loss = -delta.clip(upper=0)

#     avg_gain = gain.rolling(period).mean()
#     avg_loss = loss.rolling(period).mean()

#     rs = avg_gain / avg_loss
#     return 100 - (100 / (1 + rs))

# # ---------------- Page config ----------------
# st.set_page_config(layout="wide")
# st.title("📈 BTC/USDT – Live OHLCV Dashboard")

# # ---------------- Kafka consumer (singleton) ----------------
# @st.cache_resource
# def get_consumer():
#     c = Consumer({
#         "bootstrap.servers": "localhost:9092",
#         "group.id": "streamlit-ui",
#         "auto.offset.reset": "latest"
#     })
#     c.subscribe(["ohlcv_1m"])
#     return c

# consumer = get_consumer()
# interval = st.sidebar.selectbox(
#     "Candle Interval",
#     ["10s", "1m"]
# )

# max_candles = st.sidebar.slider(
#     "Max candles",
#     50, 300, 200
# )

# # ---------------- Session state ----------------
# if "rows" not in st.session_state:
#     st.session_state.rows = []

# status = st.empty()
# chart_placeholder = st.empty()

# # ---------------- Poll Kafka (ONCE per run) ----------------
# msg = consumer.poll(0.5)

# if msg and not msg.error():
#     candle = json.loads(msg.value().decode("utf-8"))
#     st.session_state.rows.append(candle)
#     st.session_state.rows = st.session_state.rows[-max_candles:]

# # ---------------- Render UI ----------------
# if len(st.session_state.rows) == 0:
#     status.warning("⏳ Waiting for OHLCV data from Kafka...")
# else:
#     df = pd.DataFrame(st.session_state.rows)
#     df["time"] = pd.to_datetime(df["time"], unit="ms")
#     df["rsi"] = compute_rsi(df["close"])
#     st.subheader("RSI")
#     st.line_chart(df.set_index("time")["rsi"])
#     st.subheader("Volume")
#     st.bar_chart(df.set_index("time")["volume"])



#     status.success(f"✅ Received {len(df)} candles")

#     fig = go.Figure(data=[go.Candlestick(
#         x=df["time"],
#         open=df["open"],
#         high=df["high"],
#         low=df["low"],
#         close=df["close"]
#     )])

#     fig.update_layout(
#         height=450,
#         xaxis_rangeslider_visible=False,
#         margin=dict(l=10, r=10, t=30, b=10)
#     )

#     chart_placeholder.plotly_chart(fig, width=True)
#     last = df.iloc[-1]
#     if last["rsi"] > 70:
#         st.error("⚠️ RSI Overbought")
#     elif last["rsi"] < 30:
#         st.success("🟢 RSI Oversold")


# # ---------------- Auto refresh ----------------
# time.sleep(1)
# st.rerun()


import streamlit as st
from confluent_kafka import Consumer
import json
import pandas as pd
import time
import plotly.graph_objects as go

# ===================== INDICATORS =====================

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(50)

def compute_macd(series, fast=12, slow=26, signal=9):
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()

    macd = ema_fast - ema_slow
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    hist = macd - signal_line

    return macd.fillna(0), signal_line.fillna(0), hist.fillna(0)

# ===================== STREAMLIT CONFIG =====================

st.set_page_config(layout="wide")
st.title("📈 BTC/USDT – Real-Time Analytics Dashboard")

st.sidebar.header("Controls")
max_candles = st.sidebar.slider("Max candles", 50, 300, 200)

st.sidebar.markdown("---")
st.sidebar.markdown("### Indicators")
st.sidebar.markdown("• RSI (Momentum)")
st.sidebar.markdown("• MACD (Trend)")
st.sidebar.markdown("• Volume (Strength)")

# ===================== KAFKA CONSUMER =====================

@st.cache_resource
def get_consumer():
    consumer = Consumer({
        "bootstrap.servers": "localhost:9092",
        "group.id": "streamlit-ui",
        "auto.offset.reset": "latest"
    })
    consumer.subscribe(["ohlcv_1m"])
    return consumer

consumer = get_consumer()

# ===================== SESSION STATE =====================

if "rows" not in st.session_state:
    st.session_state.rows = []

status = st.empty()

# ===================== POLL KAFKA (NON-BLOCKING) =====================

msg = consumer.poll(0.5)

if msg and not msg.error():
    candle = json.loads(msg.value().decode("utf-8"))
    st.session_state.rows.append(candle)
    st.session_state.rows = st.session_state.rows[-max_candles:]

# ===================== RENDER =====================

if len(st.session_state.rows) == 0:
    status.warning("⏳ Waiting for OHLCV data from Kafka...")
else:
    df = pd.DataFrame(st.session_state.rows)

    df["time"] = pd.to_datetime(df["time"], unit="ms")
    df["rsi"] = compute_rsi(df["close"])
    df["macd"], df["macd_signal"], df["macd_hist"] = compute_macd(df["close"])

    last = df.iloc[-1]
    status.success(f"✅ Received {len(df)} candles")

    # ===================== METRICS =====================
    m1, m2, m3 = st.columns(3)
    m1.metric("Last Close", f"{last['close']:.2f}")
    m2.metric("RSI", f"{last['rsi']:.2f}")
    m3.metric("Volume", f"{last['volume']:.4f}")

    # ===================== CANDLESTICK =====================
    fig = go.Figure(data=[go.Candlestick(
        x=df["time"],
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"]
    )])

    fig.update_layout(
        height=450,
        xaxis_rangeslider_visible=False,
        margin=dict(l=10, r=10, t=30, b=10)
    )

    st.plotly_chart(fig, use_container_width=True)

    # ===================== RSI =====================
    st.subheader("RSI")
    st.line_chart(df.set_index("time")["rsi"])

    if last["rsi"] > 70:
        st.error("⚠️ RSI Overbought")
    elif last["rsi"] < 30:
        st.success("🟢 RSI Oversold")

    # ===================== MACD =====================
    st.subheader("MACD")
    st.line_chart(df.set_index("time")[["macd", "macd_signal"]])

    if last["macd"] > last["macd_signal"]:
        st.success("📈 MACD Bullish Crossover")
    else:
        st.warning("📉 MACD Bearish")

    # ===================== VOLUME =====================
    st.subheader("Volume")
    st.bar_chart(df.set_index("time")["volume"])

# ===================== AUTO REFRESH =====================

time.sleep(1)
st.rerun()
