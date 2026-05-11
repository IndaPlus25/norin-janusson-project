from fastapi import APIRouter

from clustering.clustering_ops import create_generation_data
from data.dtos import CreateGenerationDto, GenerationResponseDto
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

router = APIRouter(tags=["generation"])


@router.post(
    "/generation",
    response_model=GenerationResponseDto,
    status_code=201,
)
def create_new_generation(payload: CreateGenerationDto):
    with DBSession.begin() as session:

        generation_id = create_generation(payload, session)
        unpopulated_generation = get_generation(generation_id, session)
        tpms_sensors = get_all_tpms_sensors(session)
        observations = get_all_observations(session)
        create_car_dtos, create_car_observation_dtos = create_generation_data(
            unpopulated_generation, tpms_sensors, observations
        )
        # TODO: WTF happened
        car_ids = populate_generation_with_cars(create_car_dtos, session)
        for dto in create_car_observation_dtos:
            dto.car_id = car_ids[dto.car_id]
        populate_generation_with_car_observations(create_car_observation_dtos, session)
        return get_generation(generation_id, session)


@router.get(
    "/generation",
    response_model=list[GenerationResponseDto],
)
def list_generations():
    with DBSession.begin() as session:
        return get_all_generations(session)
