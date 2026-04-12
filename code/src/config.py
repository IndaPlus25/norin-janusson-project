from dotenv import load_dotenv
from os import getenv

load_dotenv()

MQTT_HOST = getenv("MQTT_HOST")
MQTT_PORT = int(getenv("MQTT_PORT", "1883"))
MQTT_KEEPALIVE = int(getenv("MQTT_KEEPALIVE", "60"))
MQTT_TOPIC = getenv("MQTT_TOPIC", "tpms")

DB_URL = getenv("DB_URL", "sqlite:///tables.db")

REDIS_PORT = int(getenv("MQTT_KEEPALIVE", "6379"))
REDIS_HOST = getenv("REDIS_HOST", "localhost")
