import asyncio
import json
import os
from datetime import datetime, timezone

import websockets
from google.cloud import pubsub_v1

try:
    from google.cloud import logging as cloud_logging
except Exception:
    cloud_logging = None


SYMBOL = "btcusdc"
INTERVAL = "1h"
STREAM_URL = f"wss://stream.binance.com:9443/ws/{SYMBOL}@kline_{INTERVAL}"
LOG_FILE = "/var/log/kline/kline.log"

PROJECT_ID = os.getenv("PROJECT_ID")
TOPIC_ID = os.getenv("TOPIC_ID")

if not PROJECT_ID:
    raise RuntimeError("PROJECT_ID environment variable is not set")
if not TOPIC_ID:
    raise RuntimeError("TOPIC_ID environment variable is not set")

publisher = pubsub_v1.PublisherClient()
TOPIC_PATH = publisher.topic_path(PROJECT_ID, TOPIC_ID)

cloud_logger = None

if cloud_logging is not None:
    try:
        cloud_client = cloud_logging.Client(project=PROJECT_ID)
        cloud_logger = cloud_client.logger("kline-streamer")
    except Exception:
        cloud_logger = None


def log_event(level, event, **fields):
    ts = datetime.now(timezone.utc).isoformat()

    details = " ".join(f"{key}={value}" for key, value in fields.items())
    line = f"{ts} [{level}] {event}"

    if details:
        line += f" | {details}"

    print(line, flush=True)

    try:
        with open(LOG_FILE, "a", buffering=1) as log:
            log.write(line + "\n")
    except Exception:
        pass

    if cloud_logger is not None:
        try:
            cloud_logger.log_struct(
                {
                    "event": event,
                    "pipeline": fields.get("pipeline"),
                    "pipeline_step": fields.get("pipeline_step"),
                    "symbol": fields.get("symbol"),
                    "interval": fields.get("interval"),
                    "topic": fields.get("topic"),
                    "next_step": fields.get("next_step"),
                    "destination": fields.get("destination"),
                    "start_time": fields.get("start_time"),
                    "close_price": fields.get("close_price"),
                    "high_price": fields.get("high_price"),
                    "low_price": fields.get("low_price"),
                    "trades": fields.get("trades"),
                    "error": fields.get("error"),
                    "message": line,
                },
                severity=level,
            )
        except Exception:
            pass


async def stream_forever():
    """Reconnect loop: keep connecting to Binance and streaming klines."""
    while True:
        try:
            log_event("INFO", "Connecting to Binance WebSocket", symbol=SYMBOL.upper(), interval=INTERVAL)
            async with websockets.connect(
                STREAM_URL,
                ping_interval=20,
                ping_timeout=20,
                close_timeout=10,
            ) as websocket:
                log_event(
                    "INFO",
                    "Binance WebSocket connected",
                    pipeline_step="Binance_to_VM",
                    symbol=SYMBOL.upper(),
                    interval=INTERVAL,
                )
                async for message in websocket:
                    try:
                        data = json.loads(message)
                        kline = data.get("k")
                        if not kline:
                            continue

                        if kline.get("x"):  # closed candle
                            serialized = json.dumps(kline)
                            log_event(
                                "INFO",
                                "Closed kline received",
                                pipeline_step="Binance_to_VM",
                                symbol=kline.get("s"),
                                interval=kline.get("i"),
                                start_time=datetime.fromtimestamp(kline.get("t") / 1000, timezone.utc).isoformat(),
                                close_price=kline.get("c"),
                                high_price=kline.get("h"),
                                low_price=kline.get("l"),
                                trades=kline.get("n"),
                            )

                            future = publisher.publish(
                                TOPIC_PATH,
                                serialized.encode("utf-8"),
                                symbol=SYMBOL,
                                ingestion_type="websocket",
                                source_type="cryptocurrency_exchange",
                                source_name="binance",
                                interval=INTERVAL,
                            )
                            # wait for ack to catch publish errors
                            future.result(timeout=10)
                            log_event(
                                "INFO",
                                "Published message to Pub/Sub",
                                pipeline_step="VM_to_PubSub",
                                topic=TOPIC_ID,
                                next_step="PubSub_to_Bronze",
                                destination="bronze.market_klines",
                                symbol=SYMBOL.upper(),
                                interval=INTERVAL,
                            )
                    except Exception as e:
                        log_event(
                            "ERROR",
                            "Error while processing message",
                            pipeline_step="VM_processing",
                            error=repr(e),
                        )
        except Exception as e:
            log_event(
                "ERROR",
                "Connection error, reconnecting in 5s",
                pipeline_step="Binance_connection",
                error=repr(e),
            )
            await asyncio.sleep(5)


def main():
    log_event(
        "INFO",
        "Pipeline started",
        pipeline="Binance_to_BigQuery_Medallion",
        symbol=SYMBOL.upper(),
        interval=INTERVAL,
    )
    try:
        asyncio.run(stream_forever())
    except KeyboardInterrupt:
        log_event("INFO", "Shutting down kline streamer")


if __name__ == "__main__":
    main()
