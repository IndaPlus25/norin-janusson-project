from fastapi import APIRouter

from data.dtos import CreateObservationSensorDto, ObservationSensorResponseDto
from db.db_init import DBSession

from db.db_ops import (
    create_observation_sensor,
    get_all_observation_sensors,
    get_observation_sensor,
)

router = APIRouter(tags=["observation_sensor"])


@router.get(
    "/observation_sensor",
    response_model=list[ObservationSensorResponseDto],
)
def list_observation_sensors():
    with DBSession.begin() as session:

        return get_all_observation_sensors(session)


@router.post(
    "/observation_sensor",
    response_model=ObservationSensorResponseDto,
    status_code=201,
)
def create_new_observation_sensor(payload: CreateObservationSensorDto):
    with DBSession.begin() as session:
        observation_sensor_id = create_observation_sensor(payload, session)
        return get_observation_sensor(observation_sensor_id, session)
