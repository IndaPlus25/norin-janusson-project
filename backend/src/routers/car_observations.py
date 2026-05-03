from fastapi import APIRouter

from data.DTO_objects import CarObservationResponseDto
from db.DB_ops import get_car_observation, get_recent_car_observations_for_generation

router = APIRouter(tags=["car_observation"])


@router.get(
    "/car_observation/{car_observation_id}",
    response_model=CarObservationResponseDto,
)
def fetch_car_observation(car_observation_id: int):
    return get_car_observation(car_observation_id)


@router.get(
    "/generation/{generation_id}/timeframe/{max_age_ms}",
    response_model=list[CarObservationResponseDto],
)
def list_recent_car_observations_for_generation(generation_id: int, max_age_ms: int):
    return get_recent_car_observations_for_generation(generation_id, max_age_ms)
