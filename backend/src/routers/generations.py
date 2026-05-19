from fastapi import APIRouter

from clustering.clustering_ops import create_generation_data
from data.dtos import (
    CreateCarDto,
    CreateCarObservationDto,
    CreateGenerationDto,
    GenerationResponseDto,
)
from db.db_init import DBSession
from db.db_ops import (
    create_generation,
    get_all_generations,
    get_all_observations,
    get_all_tpms_sensors,
    get_generation,
    populate_generation_with_car_observations,
    populate_generation_with_cars,
)

PLACEHOLDER_CAR_NAME = "placeholder"

router = APIRouter(tags=["generation"])


@router.post(
    "/generation",
    response_model=GenerationResponseDto,
    status_code=201,
)
def create_new_generation(payload: CreateGenerationDto):
    with DBSession.begin() as session:
        generation_id = create_generation(payload, session)
        tpms_sensors = get_all_tpms_sensors(session)
        observations = get_all_observations(session)

        clustering_result = create_generation_data(tpms_sensors, observations)

        create_car_dtos = [
            CreateCarDto(
                name=PLACEHOLDER_CAR_NAME,
                generation_id=generation_id,
                tpms_sensor_ids=clustered_car.tpms_sensor_ids,
            )
            for clustered_car in clustering_result.cars
        ]
        car_ids = populate_generation_with_cars(create_car_dtos, session)

        create_car_observation_dtos = [
            CreateCarObservationDto(
                timestamp=clustered_car_observation.timestamp,
                car_id=car_ids[clustered_car_observation.cluster_index],
                observation_ids=clustered_car_observation.observation_ids,
                observation_sensor_id=clustered_car_observation.observation_sensor_id,
            )
            for clustered_car_observation in clustering_result.car_observations
        ]
        populate_generation_with_car_observations(create_car_observation_dtos, session)

        return get_generation(generation_id, session)


@router.get(
    "/generation",
    response_model=list[GenerationResponseDto],
)
def list_generations():
    with DBSession.begin() as session:
        return get_all_generations(session)
