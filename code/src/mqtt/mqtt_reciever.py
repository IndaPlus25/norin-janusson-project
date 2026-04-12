import paho.mqtt.client as mqtt
import json
from db.DB_ops import TPMS_sensor_exists_by_id, add_observation, create_TPMS_sensor
from config import MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE, MQTT_TOPIC
from data.DTO_objects import ObservationData, TPMSSensorData
from datetime import datetime


def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    data = json.loads(payload)
    observation_sensor_id = data["observation_sensor_id"]
    tpms_sensor_id = data["id"]
    sensor_type = data["type"]
    timestamp = datetime.fromisoformat(data["time"])

    if not TPMS_sensor_exists_by_id(tpms_sensor_id):
        create_TPMS_sensor(TPMSSensorData(tpms_sensor_id, sensor_type))

    add_observation(ObservationData(tpms_sensor_id, observation_sensor_id, timestamp))


def start_mqtt() -> None:
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE)
    client.subscribe(MQTT_TOPIC)
    client.loop_forever()
