from dataclasses import dataclass
from datetime import datetime


@dataclass
class ClusteredCar:
    tpms_sensor_ids: list[str]


@dataclass
class ClusteredCarObservation:
  
    cluster_index: int
    timestamp: datetime
    observation_ids: list[int]
    observation_sensor_id: str


@dataclass
class ClusteringResult:
    cars: list[ClusteredCar]
    car_observations: list[ClusteredCarObservation]
