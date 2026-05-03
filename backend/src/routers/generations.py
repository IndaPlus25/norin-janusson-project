from fastapi import APIRouter

from clustering.clustering_ops import create_generation_data
from data.DTO_objects import CreateGenerationDto, GenerationResponseDto
from db.DB_ops import (
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
    generation_id = create_generation(payload)
    unpopulated_generation = get_generation(generation_id)
    tpms_sensors = get_all_tpms_sensors()
    observations = get_all_observations()
    create_car_dtos, create_car_observation_dtos = create_generation_data(
        unpopulated_generation, tpms_sensors, observations
    )
    # TODO: WTF happened
    car_ids = populate_generation_with_cars(create_car_dtos)
    for dto in create_car_observation_dtos:
        dto.car_id = car_ids[dto.car_id]
    populate_generation_with_car_observations(create_car_observation_dtos)
    populated_generation = get_generation(generation_id)
    return populated_generation


@router.get(
    "/generation",
    response_model=list[GenerationResponseDto],
)
def list_generations():
    return get_all_generations()
