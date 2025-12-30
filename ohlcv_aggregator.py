import json
import time
from confluent_kafka import Consumer, Producer

# ---------------- CONFIG ----------------
KAFKA_BOOTSTRAP = "localhost:9092"
RAW_TOPIC = "raw_ticks"
OHLCV_TOPIC = "ohlcv_1m"

# ---------------- CONSUMER ----------------
consumer = Consumer({
    "bootstrap.servers": KAFKA_BOOTSTRAP,
    "group.id": "ohlcv-aggregator",
    "auto.offset.reset": "latest"
})

consumer.subscribe([RAW_TOPIC])

# ---------------- PRODUCER ----------------
producer = Producer({
    "bootstrap.servers": KAFKA_BOOTSTRAP
})

def delivery_report(err, msg):
    if err:
        print("Delivery failed:", err)

# ---------------- AGGREGATION ----------------
bucket = []
start = time.time()

print("Starting OHLCV aggregator...")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print("Consumer error:", msg.error())
            continue

        tick = json.loads(msg.value().decode("utf-8"))
        bucket.append(tick)

        if time.time() - start >= 10 and bucket:
            prices = [x["price"] for x in bucket]
            volumes = [x["volume"] for x in bucket]

            candle = {
                "time": int(time.time() * 1000),
                "open": prices[0],
                "high": max(prices),
                "low": min(prices),
                "close": prices[-1],
                "volume": sum(volumes)
            }

            producer.produce(
                OHLCV_TOPIC,
                value=json.dumps(candle),
                callback=delivery_report
            )
            producer.flush()

            print("OHLCV:", candle)

            bucket = []
            start = time.time()

except KeyboardInterrupt:
    print("Stopping aggregator...")

finally:
    consumer.close()
