from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
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


@dataclass
class ObservationData:
    tpms_sensor_id: str
    observation_sensor_id: str
    timestamp: datetime


@dataclass
class TPMSSensorFormatted:
    id: str
    sensor_type: str
    observations: dict[str, list[datetime]]


@dataclass
class TPMSSensorFormatted:
    def __init__(
        self, id: str, sensor_type: str, observations: dict[str, list[datetime]]
    ):
        self.id: str = id
        self.sensor_type: str = sensor_type
        self.observations: dict[str, list[datetime]] = observations


class Observation(Base):
    __tablename__ = "observations"

    id: Mapped[int] = mapped_column(primary_key=True)
    observation_sensor_id: Mapped[str]
    timestamp: Mapped[datetime]
    tpms_sensor_id: Mapped[str] = mapped_column(ForeignKey("tpms_sensors.id"))
    sensor: Mapped["TPMSSensor"] = relationship(back_populates="observations")

    pruned_observations: Mapped[list["PrunedObservation"]] = relationship(
        secondary=pruned_observation_association, back_populates="observations"
    )


class TPMSSensor(Base):
    __tablename__ = "tpms_sensors"

    id: Mapped[str] = mapped_column(primary_key=True)
    sensor_type: Mapped[str]

    observations: Mapped[list["Observation"]] = relationship(back_populates="sensor")
    cars: Mapped[list["Car"]] = relationship(
        secondary=car_sensor_association, back_populates="tpms_sensors"
    )


class Car(Base):
    __tablename__ = "cars"

    id: Mapped[str] = mapped_column(primary_key=True)
    generation: Mapped[int]
    tpms_sensors: Mapped[list["TPMSSensor"]] = relationship(
        secondary=car_sensor_association, back_populates="cars"
    )
    pruned_observations: Mapped[list["PrunedObservation"]] = relationship(
        back_populates="car"
    )


class PrunedObservation(Base):
    __tablename__ = "pruned_observations"

    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime]
    car_id: Mapped[str] = mapped_column(ForeignKey("cars.id"))
    car: Mapped["Car"] = relationship(back_populates="pruned_observations")
    observations: Mapped[list["Observation"]] = relationship(
        secondary=pruned_observation_association, back_populates="pruned_observations"
    )


def format_sensor(sensor: TPMSSensor) -> TPMSSensorFormatted:
    obs_dict: dict[str, list[datetime]] = defaultdict(list)
    for obs in sensor.observations:
        obs_dict[obs.observation_sensor_id].append(obs.timestamp)

    return TPMSSensorFormatted(
        id=sensor.id,
        sensor_type=sensor.sensor_type,
        observations=dict(obs_dict),
    )
