from datetime import datetime
from dataclasses import dataclass

from data.DB_models import EPSG


@dataclass
class TPMSSensorFormatted:
    id: str
    sensor_type: str
    observations: dict[str, list[datetime]]


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
    adress: str


@dataclass
class CreateGenerationDto:
    created_at: datetime
    name: str


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


@dataclass
class CarResponseDto:
    id: int
    name: str
    generation_id: int
    tpms_sensor_ids: list[str]
    car_observation_ids: list[int]


@dataclass
class ObservationSensorResponseDto:
    id: str
    name: str
    lat: float
    lng: float
    epsg: EPSG
    adress: str
    active: bool
    observation_ids: list[int]
    car_observation_ids: list[int]


@dataclass
class ObservationResponseDto:
    id: int
    timestamp: datetime
    observation_sensor_id: str
    tpms_sensor_id: str
    car_observation_ids: list[int]


@dataclass
class CarObservationResponseDto:
    id: int
    timestamp: datetime
    car_id: int
    observation_ids: list[int]
    observation_sensor_id: int


@dataclass
class TPMSSensorResponseDto:
    id: str
    sensor_type: str
    observation_ids: list[int]
    car_ids: list[int]


@dataclass
class GenerationResponseDto:
    id: int
    created_at: datetime
    name: str
    car_ids: list[int]
