from db.DB_init import Base, engine
from data.classes import ObservationData, TPMSSensorData
from mqtt.mqtt_reciever import start_mqtt

Base.metadata.create_all(engine)

start_mqtt()
