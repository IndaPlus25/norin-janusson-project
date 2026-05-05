from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from config import ALLOWED_ORIGINS, DB_URL, IS_DEV
from db.DB_init import Base, engine
from mqtt.mqtt_receiver import start_mqtt
from db.DB_models import (
    Car,
    Generation,
    Observation,
    CarObservation,
    ObservationSensor,
    TPMSSensor,
)
from routers import observation_sensors, generations, cars, car_observations, trajectory_inference


def _wipe_dev_sqlite_db() -> None:
    if not DB_URL.startswith("sqlite:///"):
        return
    db_path = Path(DB_URL.removeprefix("sqlite:///"))
    for path in db_path.parent.glob(db_path.name + "*"):
        path.unlink()


@asynccontextmanager
async def lifespan(app: FastAPI):
    if IS_DEV:
        _wipe_dev_sqlite_db()
        engine.dispose()
    Base.metadata.create_all(engine)
    start_mqtt()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(observation_sensors.router)
app.include_router(generations.router)
app.include_router(cars.router)
app.include_router(car_observations.router)
app.include_router(trajectory_inference.router)
