import json
import sys
import threading
import time
import traceback
from dataclasses import asdict
from datetime import timezone

import paho.mqtt.client as mqtt

from config import (
    MAX_MQTT_RECONNECT_DELAY,
    MIN_MQTT_RECONNECT_DELAY,
    MQTT_HOST,
    MQTT_PORT,
    MQTT_KEEPALIVE,
    MQTT_TOPIC,
    TPMS_CLUSTER_WINDOW,
)

from data.dtos import (
    CarObservationUpdatedEvent,
    CarResponseDto,
    CreateCarObservationDto,
    CreateObservationDto,
    CreateTPMSSensorDto,
    ObservationSensorBroadcast,
)
from db.db_init import DBSession
from db.db_models import ObservationSensor, TPMSSensor
from db.db_ops import (
    append_observation_to_car_observation,
    create_car_observation,
    create_observation,
    create_tpms_sensor,
    get_car_observation,
    get_cars_for_tpms,
)
from redis_cache.init_redis import redis_client


_LOCK_SENTINEL = "creating"
_LOCK_POLL_ATTEMPTS = 20
_LOCK_POLL_INTERVAL_S = 0.05


def _wait_for_lock_holder(redis_key: str) -> int | None:
    for _ in range(_LOCK_POLL_ATTEMPTS):
        value = redis_client.get(redis_key)
        if value is not None and value != _LOCK_SENTINEL:
            return int(value)
        time.sleep(_LOCK_POLL_INTERVAL_S)
    return None


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
    observation_sensor_broadcast: ObservationSensorBroadcast = (
        ObservationSensorBroadcast.model_validate_json(msg.payload.decode())
    )

    timestamp = observation_sensor_broadcast.timestamp
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)

    publishes: list[tuple[str, str]] = []
    redis_sets: list[tuple[str, int]] = []
    redis_refreshes: list[str] = []

    with DBSession.begin() as session:
        if (
            session.get(
                ObservationSensor, observation_sensor_broadcast.observation_sensor_id
            )
            is None
        ):
            return

        if session.get(TPMSSensor, observation_sensor_broadcast.tpms_sensor_id) is None:
            create_tpms_sensor(
                CreateTPMSSensorDto(
                    observation_sensor_broadcast.tpms_sensor_id,
                    observation_sensor_broadcast.sensor_type,
                ),
                session,
            )

        observation_id: int = create_observation(
            CreateObservationDto(
                observation_sensor_broadcast.tpms_sensor_id,
                observation_sensor_broadcast.observation_sensor_id,
                timestamp,
            ),
            session,
        )

        car_responses: list[CarResponseDto] = get_cars_for_tpms(
            observation_sensor_broadcast.tpms_sensor_id, session
        )
        for car_response in car_responses:
            redis_key = f"car-sensor:{car_response.id}:{observation_sensor_broadcast.observation_sensor_id}"
            cached_car_observation_id = redis_client.get(redis_key)

            if (
                cached_car_observation_id is not None
                and cached_car_observation_id != _LOCK_SENTINEL
            ):
                car_observation_id = int(cached_car_observation_id)
                append_observation_to_car_observation(
                    car_observation_id, observation_id, session
                )
                redis_refreshes.append(redis_key)

                publishes.append(
                    (
                        generation_car_observation_updated_topic(
                            car_response.generation_id, car_response.id
                        ),
                        CarObservationUpdatedEvent(
                            car_observation_id=car_observation_id,
                            observation_id=observation_id,
                        ).model_dump_json(),
                    )
                )
            elif redis_client.set(
                redis_key, _LOCK_SENTINEL, nx=True, ex=TPMS_CLUSTER_WINDOW
            ):
                new_car_observation_id = create_car_observation(
                    CreateCarObservationDto(
                        timestamp,
                        car_response.id,
                        [observation_id],
                        observation_sensor_broadcast.observation_sensor_id,
                    ),
                    session,
                )
                car_observation = get_car_observation(new_car_observation_id, session)
                redis_sets.append((redis_key, new_car_observation_id))

                publishes.append(
                    (
                        generation_car_observation_created_topic(
                            car_response.generation_id, car_response.id
                        ),
                        json.dumps(asdict(car_observation), default=str),
                    )
                )
            else:
                existing_id = _wait_for_lock_holder(redis_key)
                if existing_id is None:
                    continue
                append_observation_to_car_observation(
                    existing_id, observation_id, session
                )
                redis_refreshes.append(redis_key)

                publishes.append(
                    (
                        generation_car_observation_updated_topic(
                            car_response.generation_id, car_response.id
                        ),
                        CarObservationUpdatedEvent(
                            car_observation_id=existing_id,
                            observation_id=observation_id,
                        ).model_dump_json(),
                    )
                )

    for key, value in redis_sets:
        redis_client.set(key, value, ex=TPMS_CLUSTER_WINDOW)
    for key in redis_refreshes:
        redis_client.expire(key, TPMS_CLUSTER_WINDOW)
    for topic, payload in publishes:
        client.publish(topic, payload)


def start_mqtt() -> None:
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = _on_connect
    client.on_disconnect = _on_disconnect
    client.reconnect_delay_set(
        min_delay=MIN_MQTT_RECONNECT_DELAY, max_delay=MAX_MQTT_RECONNECT_DELAY
    )

    def _connect_with_retry() -> None:
        delay = MIN_MQTT_RECONNECT_DELAY
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
                delay = min(delay * 2, MAX_MQTT_RECONNECT_DELAY)

    threading.Thread(target=_connect_with_retry, daemon=True).start()


def generation_car_observation_created_topic(generation_id: int, car_id: int) -> str:
    return f"generation/{generation_id}/car/{car_id}/car-observation/created"


def generation_car_observation_updated_topic(generation_id: int, car_id: int) -> str:
    return f"generation/{generation_id}/car/{car_id}/car-observation/updated"
