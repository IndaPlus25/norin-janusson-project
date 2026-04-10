from dataclasses import dataclass
from datetime import datetime
from collections import defaultdict
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from db.DB_init import Base


@dataclass
class ObservationData:
    tpms_sensor_id: str
    observation_sensor_id: str
    timestamp: datetime


class Observation(Base):
    __tablename__ = "observations"

    id: Mapped[int] = mapped_column(primary_key=True)
    tpms_sensor_id: Mapped[str] = mapped_column(ForeignKey("tpms_sensors.id"))
    observation_sensor_id: Mapped[str]
    timestamp: Mapped[datetime]
    sensor: Mapped["TPMSSensor"] = relationship(back_populates="observations")


@dataclass
class TPMSSensorData:
    id: str
    sensor_type: str


class TPMSSensor(Base):
    __tablename__ = "tpms_sensors"

    id: Mapped[str] = mapped_column(primary_key=True)
    sensor_type: Mapped[str]
    observations: Mapped[list["Observation"]] = relationship(back_populates="sensor")


class TPMSsensorFormatted:
    def __init__(
        self, id: str, sensor_type: str, observations: dict[str, list[datetime]]
    ):
        self.id: str = id
        self.sensor_type: str = sensor_type
        self.observations: dict[str, list[datetime]] = observations


def format_sensor(sensor: TPMSSensor) -> TPMSsensorFormatted:
    obs_dict: dict[str, list[datetime]] = defaultdict(list)
    for obs in sensor.observations:
        obs_dict[obs.observation_sensor_id].append(obs.timestamp)

    return TPMSsensorFormatted(
        id=sensor.id, sensor_type=sensor.sensor_type, observations=dict(obs_dict)
    )
