from dataclasses import asdict

import paho.mqtt.client as mqtt
import json
from redis_cache.init_redis import redis_client
from db.DB_ops import (
    TPMS_sensor_exists_by_id,
    append_observation_to_car_observation,
    create_car_observation,
    create_observation,
    create_TPMS_sensor,
    get_car_observation,
    get_cars_for_tpms,
)
from config import MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE, MQTT_TOPIC
from data.DTO_objects import (
    CarResponseDto,
    CreateCarObservationDto,
    CreateObservationDto,
    CreateTPMSSensorDto,
)
from datetime import datetime


def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    data = json.loads(payload)
    observation_sensor_id = data["observation_sensor_id"]
    tpms_sensor_id = data["id"]
    sensor_type = data["type"]
    timestamp = datetime.fromisoformat(data["time"])

    if not TPMS_sensor_exists_by_id(tpms_sensor_id):
        create_TPMS_sensor(CreateTPMSSensorDto(tpms_sensor_id, sensor_type))

    observation_id: int = create_observation(
        CreateObservationDto(tpms_sensor_id, observation_sensor_id, timestamp)
    )

    car_responses: list[CarResponseDto] = get_cars_for_tpms(tpms_sensor_id)

    for car_response in car_responses:
        redis_key: str = f"car-sensor:{car_response.id}:{observation_sensor_id}"
        car_observation_id = redis_client.get(redis_key)

        if car_observation_id is None:
            new_car_observation_id = create_car_observation(
                CreateCarObservationDto(
                    timestamp, car_response.id, [observation_id], observation_sensor_id
                )
            )
            redis_client.set(redis_key, new_car_observation_id, ex=90)
            topic = make_topic_created(car_response.generation_id, car_response.id)
            outgoing_payload = json.dumps(
                asdict(get_car_observation(new_car_observation_id)), default=str
            )
            client.publish(topic, outgoing_payload)

        else:
            append_observation_to_car_observation(
                int(car_observation_id), observation_id
            )
            redis_client.expire(redis_key, 90)
            topic = make_topic_updated(car_response.generation_id, car_response.id)
            outgoing_payload = json.dumps(
                {
                    "car_observation_id": int(car_observation_id),
                    "observation_id": observation_id,
                }
            )
            client.publish(topic, outgoing_payload)


def start_mqtt() -> None:
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE)
    client.subscribe(MQTT_TOPIC)
    client.loop_start()


def make_topic_updated(generation_id: int, car_id: int) -> str:
    return f"generation/{generation_id}/car/{car_id}/car-observation/updated"


def make_topic_created(generation_id: int, car_id: int) -> str:
    return f"generation/{generation_id}/car/{car_id}/car-observation/created"
