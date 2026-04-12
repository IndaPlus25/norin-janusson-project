from datetime import datetime
from dataclasses import dataclass

# TODO: enforce "not empty" for DTOs?


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
class TPMSSensorData:
    id: str
    sensor_type: str
