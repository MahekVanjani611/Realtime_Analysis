# import asyncio, json
# import websockets
# from kafka import KafkaProducer

# producer = KafkaProducer(
#     bootstrap_servers="localhost:9092",
#     value_serializer=lambda v: json.dumps(v).encode()
# )

# async def main():
#     url = "wss://stream.binance.com:9443/ws/btcusdt@trade"

#     async with websockets.connect(url) as ws:
#         print("Connected to Binance WS")
#         while True:
#             msg = json.loads(await ws.recv())
#             producer.send("raw_ticks", {
#                 "price": float(msg["p"]),
#                 "volume": float(msg["q"]),
#                 "timestamp": msg["T"]
#             })

# asyncio.run(main())
import asyncio
import json
import websockets
from confluent_kafka import Producer

# Kafka config
producer = Producer({
    "bootstrap.servers": "localhost:9092"
})

def delivery_report(err, msg):
    if err is not None:
        print("Delivery failed:", err)
    else:
        pass  # keep silent for speed

async def stream_to_kafka():
    url = "wss://stream.binance.com:9443/ws/btcusdt@trade"

    async with websockets.connect(url) as ws:
        print("Connected to Binance WebSocket → Kafka")

        while True:
            data = await ws.recv()
            trade = json.loads(data)

            message = {
                "symbol": trade["s"],
                "price": float(trade["p"]),
                "volume": float(trade["q"]),
                "timestamp": trade["T"]
            }

            producer.produce(
                topic="raw_ticks",
                value=json.dumps(message),
                callback=delivery_report
            )
            producer.poll(0)

            print("Sent:", message)

asyncio.run(stream_to_kafka())
