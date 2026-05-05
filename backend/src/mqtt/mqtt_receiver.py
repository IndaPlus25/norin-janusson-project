import json
import sys
import threading
import time
import traceback
from dataclasses import asdict
from datetime import datetime, timezone

import paho.mqtt.client as mqtt

from config import MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE, MQTT_TOPIC
from data.DTO_objects import (
    CarResponseDto,
    CreateCarObservationDto,
    CreateObservationDto,
    CreateTPMSSensorDto,
)
from db.DB_ops import (
    TPMS_sensor_exists_by_id,
    append_observation_to_car_observation,
    create_car_observation,
    create_observation,
    create_TPMS_sensor,
    get_car_observation,
    get_cars_for_tpms,
    observation_sensor_exists_by_id,
)
from redis_cache.init_redis import redis_client


def on_message(client, userdata, msg):
    try:
        _process_message(client, msg)
    except Exception:
        print("mqtt receiver: failed to read message", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)


def _on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.subscribe(MQTT_TOPIC)
        print(f"mqtt receiver: connected and subscribed to {MQTT_TOPIC}")
    else:
        print(f"mqtt receiver: connect returned {rc}", file=sys.stderr)


def _on_disconnect(client, userdata, rc):
    if rc != 0:
        print(f"mqtt receiver: disconnected {rc}", file=sys.stderr)


def _process_message(client, msg):
    data = json.loads(msg.payload.decode())
    observation_sensor_id = data["observation_sensor_id"]
    tpms_sensor_id = data["id"]
    sensor_type = data["type"]
    timestamp = datetime.fromisoformat(data["time"])
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)

    if not observation_sensor_exists_by_id(observation_sensor_id):
        return

    if not TPMS_sensor_exists_by_id(tpms_sensor_id):
        create_TPMS_sensor(CreateTPMSSensorDto(tpms_sensor_id, sensor_type))

    observation_id: int = create_observation(
        CreateObservationDto(tpms_sensor_id, observation_sensor_id, timestamp)
    )

    client.publish(
        observation_sensor_observation_created_topic(observation_sensor_id),
        json.dumps({"observation_id": observation_id}),
    )

    car_responses: list[CarResponseDto] = get_cars_for_tpms(tpms_sensor_id)
    for car_response in car_responses:
        redis_key = f"car-sensor:{car_response.id}:{observation_sensor_id}"
        cached_car_observation_id = redis_client.get(redis_key)

        if cached_car_observation_id is None:
            new_car_observation_id = create_car_observation(
                CreateCarObservationDto(
                    timestamp, car_response.id, [observation_id], observation_sensor_id
                )
            )
            redis_client.set(redis_key, new_car_observation_id, ex=90)

            client.publish(
                generation_car_observation_created_topic(
                    car_response.generation_id, car_response.id
                ),
                json.dumps(
                    asdict(get_car_observation(new_car_observation_id)), default=str
                ),
            )
            #TODO: very ugly that we send essentially the same data in two separate topics, we should probably rework to have only one topic for created car observations. 

            client.publish(
                observation_sensor_car_observation_created_topic(observation_sensor_id),
                json.dumps({"car_observation_id": new_car_observation_id}),
            )

        else:
            car_observation_id = int(cached_car_observation_id)
            append_observation_to_car_observation(car_observation_id, observation_id)
            redis_client.expire(redis_key, 90)

            client.publish(
                generation_car_observation_updated_topic(
                    car_response.generation_id, car_response.id
                ),
                json.dumps(
                    {
                        "car_observation_id": car_observation_id,
                        "observation_id": observation_id,
                    }
                ),
            )


def start_mqtt() -> None:
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = _on_connect
    client.on_disconnect = _on_disconnect
    client.reconnect_delay_set(min_delay=1, max_delay=60)

    def _connect_with_retry() -> None:
        delay = 1
        while True:
            try:
                client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE)
                client.loop_start()
                return
            except Exception:
                print(
                    f"mqtt receiver: connect failed, retrying in {delay}s",
                    file=sys.stderr,
                )
                traceback.print_exc(file=sys.stderr)
                time.sleep(delay)
                delay = min(delay * 2, 60)

    threading.Thread(target=_connect_with_retry, daemon=True).start()


def generation_car_observation_created_topic(generation_id: int, car_id: int) -> str:
    return f"generation/{generation_id}/car/{car_id}/car-observation/created"


def generation_car_observation_updated_topic(generation_id: int, car_id: int) -> str:
    return f"generation/{generation_id}/car/{car_id}/car-observation/updated"


def observation_sensor_observation_created_topic(observation_sensor_id: str) -> str:
    return f"observation-sensor/{observation_sensor_id}/observation/created"

def observation_sensor_car_observation_created_topic(
    observation_sensor_id: str,
) -> str:
    return f"observation-sensor/{observation_sensor_id}/car-observation/created"
