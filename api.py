from fastapi import FastAPI, WebSocket
from confluent_kafka import Consumer
import json
import asyncio

app = FastAPI()

KAFKA_BOOTSTRAP = "localhost:9092"
TOPIC = "ohlcv_1m"


def create_consumer():
    return Consumer({
        "bootstrap.servers": KAFKA_BOOTSTRAP,
        "group.id": "fastapi-ws-consumer",
        "auto.offset.reset": "latest"
    })


@app.websocket("/ws/live")
async def ws_live(ws: WebSocket):
    await ws.accept()
    consumer = create_consumer()
    consumer.subscribe([TOPIC])

    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                await asyncio.sleep(0.1)
                continue

            if msg.error():
                print("Kafka error:", msg.error())
                continue

            data = json.loads(msg.value().decode("utf-8"))
            await ws.send_json(data)

    except Exception as e:
        print("WebSocket closed:", e)

    finally:
        consumer.close()
