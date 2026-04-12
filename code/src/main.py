from db.DB_init import Base, engine
from mqtt.mqtt_reciever import start_mqtt
from data.DB_models import (
    Car,
    Generation,
    Observation,
    PrunedObservation,
    ObservationSensor,
    TPMSSensor,
)

Base.metadata.create_all(engine)

start_mqtt()
