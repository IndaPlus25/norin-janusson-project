from sqlalchemy import Column, ForeignKey, Index, Table
from db.DB_init import Base

car_sensor_association = Table(
    "car_sensor",
    Base.metadata,
    Column("car_id", ForeignKey("cars.id"), primary_key=True),
    Column("tpms_sensor_id", ForeignKey("tpms_sensors.id"), primary_key=True),
    Index("ix_car_sensor_tpms_sensor", "tpms_sensor_id"),
)

car_observation_association = Table(
    "car_observation_association",
    Base.metadata,
    Column("observation_id", ForeignKey("observations.id"), primary_key=True),
    Column("car_observation_id", ForeignKey("car_observations.id"), primary_key=True),
)
