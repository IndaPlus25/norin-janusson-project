from datetime import datetime
from dataclasses import dataclass


@dataclass
class CreateObservationDto:
    tpms_sensor_id: str
    observation_sensor_id: str
    timestamp: datetime


@dataclass
class CreateTPMSSensorDto:
    id: str
    sensor_type: str


@dataclass
class CreateObservationSensorDto:
    id: str
    name: str
    lat: float
    lng: float


@dataclass
class CreateGenerationDto:
    created_at: datetime
    name: str


@dataclass
class TPMSSensorFormatted:
    id: str
    sensor_type: str
    observations: dict[str, list[datetime]]


@dataclass
class CreateCarDto:
    name: str
    generation_id: int
    tpms_sensor_ids: list[str]


@dataclass
class CreateCarObservationDto:
    timestamp: datetime
    car_id: int
    observation_ids: list[int]
    observation_sensor_id: str
