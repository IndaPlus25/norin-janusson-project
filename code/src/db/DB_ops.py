from sqlalchemy import exists, text
from db.DB_init import DBSession, inspector
from data.DB_models import Car, Generation, Observation, ObservationSensor, TPMSSensor
from data.DTO_objects import (
    CreateCarDto,
    CreateGenerationDto,
    CreateObservationDto,
    CreateObservationSensorDto,
    CreateTPMSSensorDto,
)

# TODO: create validation checks on data


def print_db() -> None:

    with DBSession() as session:
        for table_name in inspector.get_table_names():
            print(f"\n=== {table_name} ===")
            result = session.execute(text(f"SELECT * FROM {table_name}"))
            rows = result.fetchall()
            if not rows:
                print("  (empty)")
            for row in rows:
                print(" ", row)


def TPMS_sensor_exists_by_id(id: str) -> bool:
    with DBSession() as session:
        return session.query(exists().where(TPMSSensor.id == id)).scalar()


def create_TPMS_sensor(dto: CreateTPMSSensorDto) -> str:
    with DBSession() as session:
        tpms_sensor = TPMSSensor.from_dto(dto)
        session.add(tpms_sensor)
        session.commit()
        return tpms_sensor.id


def create_observation(dto: CreateObservationDto) -> int:
    with DBSession() as session:
        observation = Observation.from_dto(dto)
        session.add(observation)
        session.commit()
        return observation.id


def create_observation_sensor(dto: CreateObservationSensorDto) -> str:
    with DBSession() as session:
        observation_sensor = ObservationSensor.from_dto(dto)
        session.add(observation_sensor)
        session.commit()
        return observation_sensor.id


def create_generation(dto: CreateGenerationDto) -> int:
    with DBSession() as session:
        generation = Generation.from_dto(dto)
        session.add(generation)
        session.commit()
        return generation.id


def create_car(dto: CreateCarDto) -> int:
    with DBSession() as session:
        tpms_sensors = (
            session.query(TPMSSensor)
            .filter(TPMSSensor.id.in_(dto.tpms_sensor_ids))
            .all()
        )
        car = Car.from_dto(dto, tpms_sensors)
        session.add(car)
        session.commit()
        return car.id
