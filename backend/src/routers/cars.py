from fastapi import APIRouter

from data.DTO_objects import CarResponseDto
from db.DB_ops import get_cars_for_generation, update_car_name
from pydantic import BaseModel, Field


class RenameCarPayload(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)


router = APIRouter(tags=["car"])


@router.get(
    "/generation/{generation_id}/car",
    response_model=list[CarResponseDto],
)
def list_cars_for_generation(generation_id: int):
    return get_cars_for_generation(generation_id)


@router.patch("/car/{car_id}/name", response_model=CarResponseDto)
def rename_car(car_id: int, payload: RenameCarPayload):
    return update_car_name(car_id, payload.name)
