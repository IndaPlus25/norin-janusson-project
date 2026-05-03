from datetime import datetime
from dataclasses import dataclass
from data.enums import EPSG


def _require_non_empty_id(value: str, field: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field} must be non-empty")


@dataclass
class CreateObservationDto:
    tpms_sensor_id: str
    observation_sensor_id: str
    timestamp: datetime

    def __post_init__(self) -> None:
        _require_non_empty_id(self.tpms_sensor_id, "tpms_sensor_id")
        _require_non_empty_id(self.observation_sensor_id, "observation_sensor_id")


@dataclass
class CreateTPMSSensorDto:
    id: str
    sensor_type: str

    def __post_init__(self) -> None:
        _require_non_empty_id(self.id, "id")


@dataclass
class CreateObservationSensorDto:
    id: str
    name: str
    lat: float
    lng: float
    address: str
    epsg: EPSG = EPSG.STANDARD

    def __post_init__(self) -> None:
        _require_non_empty_id(self.id, "id")


@dataclass
class CreateGenerationDto:
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

    def __post_init__(self) -> None:
        _require_non_empty_id(self.observation_sensor_id, "observation_sensor_id")


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
    address: str
    active: bool
    observation_ids: list[int]
    car_observation_ids: list[int]


@dataclass
class CarObservationResponseDto:
    id: int
    timestamp: datetime
    car_id: int
    observation_ids: list[int]
    observation_sensor_id: str


@dataclass
class TPMSSensorResponseDto:
    id: str
    sensor_type: str
    observation_ids: list[int]
    car_ids: list[int]


@dataclass
class ObservationResponseDto:
    id: int
    timestamp: datetime
    observation_sensor_id: str
    tpms_sensor_id: str
    car_observation_ids: list[int]


@dataclass
class GenerationResponseDto:
    id: int
    created_at: datetime
    name: str
    car_ids: list[int]
