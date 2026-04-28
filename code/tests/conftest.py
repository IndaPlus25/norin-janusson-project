from os import environ

environ["MQTT_HOST"] = "test-broker"
environ["MQTT_PORT"] = "1883"
environ["MQTT_KEEPALIVE"] = "60"
environ["MQTT_TOPIC"] = "tpms-test"
environ["DB_URL"] = "sqlite:///:memory:"
environ["REDIS_HOST"] = "localhost"
environ["REDIS_PORT"] = "6379"

import pytest
from db.DB_init import Base, engine

from data.DB_models import (
    Car,
    Generation,
    Observation,
    CarObservation,
    ObservationSensor,
    TPMSSensor,
)


@pytest.fixture(autouse=True)
def _create_schema():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)
