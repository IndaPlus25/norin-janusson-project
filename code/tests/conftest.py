from os import environ

environ["MQTT_HOST"] = "test-broker"
environ["MQTT_PORT"] = "1883"
environ["MQTT_KEEPALIVE"] = "60"
environ["MQTT_TOPIC"] = "tpms-test"
environ["DB_URL"] = "sqlite:///:memory:"
environ["REDIS_HOST"] = "localhost"
environ["REDIS_PORT"] = "6379"
