from fastapi import APIRouter

from data.dtos import CarObservationResponseDto
from db.db_init import DBSession
from db.db_ops import get_car_observation, get_recent_car_observations_for_generation

router = APIRouter(tags=["car_observation"])


@router.get(
    "/car_observation/{car_observation_id}",
    response_model=CarObservationResponseDto,
)
def fetch_car_observation(car_observation_id: int):
    with DBSession.begin() as session:
        return get_car_observation(car_observation_id, session)


@router.get(
    "/generation/{generation_id}/timeframe/{max_age_ms}",
    response_model=list[CarObservationResponseDto],
)
def list_recent_car_observations_for_generation(generation_id: int, max_age_ms: int):
    with DBSession.begin() as session:
        return get_recent_car_observations_for_generation(
            generation_id, max_age_ms, session
        )
