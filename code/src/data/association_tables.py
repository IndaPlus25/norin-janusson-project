from sqlalchemy import Column, ForeignKey, Table
from db.DB_init import Base

car_sensor_association = Table(
    "car_sensor",
    Base.metadata,
    Column("car_id", ForeignKey("cars.id"), primary_key=True),
    Column("tpms_sensor_id", ForeignKey("tpms_sensors.id"), primary_key=True),
)

pruned_observation_association = Table(
    "observation_pruned_observation",
    Base.metadata,
    Column("observation_id", ForeignKey("observations.id"), primary_key=True),
    Column(
        "pruned_observation_id", ForeignKey("pruned_observations.id"), primary_key=True
    ),
)