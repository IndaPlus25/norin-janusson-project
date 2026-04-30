from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import ALLOWED_ORIGINS
from db.DB_init import Base, engine
from mqtt.mqtt_receiver import start_mqtt
from data.DB_models import (
    Car,
    Generation,
    Observation,
    CarObservation,
    ObservationSensor,
    TPMSSensor,
)
from routers import observation_sensors, generations, cars, car_observations


@asynccontextmanager
async def lifespan(app: FastAPI):
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
