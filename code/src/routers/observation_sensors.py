from fastapi import APIRouter

from data.DTO_objects import CreateObservationSensorDto, ObservationSensorResponseDto
from db.DB_ops import create_observation_sensor, get_all_observation_sensors, get_observation_sensor

router = APIRouter( tags=["observation_sensor"])

@router.get(
    "/observation_sensor",
    response_model=list[ObservationSensorResponseDto],
)
def list_observation_sensors():
    return get_all_observation_sensors()

@router.post(
    "/observation_sensor",
    response_model=ObservationSensorResponseDto,
    status_code=201,
)
def create_new_observation_sensor(payload: CreateObservationSensorDto):
    observation_sensor_id = create_observation_sensor(payload)
    return get_observation_sensor(observation_sensor_id)