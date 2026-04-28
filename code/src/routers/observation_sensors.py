from fastapi import APIRouter

from data.DTO_objects import CreateObservationSensorDto
from db.DB_ops import create_observation_sensor, get_all_observation_sensors, get_observation_sensor

router = APIRouter(prefix="/observation_sensors", tags=["observation_sensors"])

@router.get("")
def list_observation_sensors():
    return get_all_observation_sensors()

@router.post("", status_code=201)
def create_new_observation_sensor(payload: CreateObservationSensorDto):
    observation_sensor_id = create_observation_sensor(payload)
    return get_observation_sensor(observation_sensor_id)