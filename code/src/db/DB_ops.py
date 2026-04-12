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
        if session.get(TPMSSensor, dto.id) is not None:
            raise ValueError(f"TPMS sensor with id {dto.id} already exists")

        tpms_sensor = TPMSSensor.from_dto(dto)
        session.add(tpms_sensor)
        session.commit()
        return tpms_sensor.id


def create_observation(dto: CreateObservationDto) -> int:
    with DBSession() as session:
        if session.get(TPMSSensor, dto.tpms_sensor_id) is None:
            raise ValueError(f"TPMS sensor {dto.tpms_sensor_id} does not exist")
        if session.get(ObservationSensor, dto.observation_sensor_id) is None:
            raise ValueError(
                f"Observation sensor {dto.observation_sensor_id} does not exist"
            )

        observation = Observation.from_dto(dto)
        session.add(observation)
        session.commit()
        return observation.id


def create_observation_sensor(dto: CreateObservationSensorDto) -> str:
    with DBSession() as session:
        if session.get(ObservationSensor, dto.id) is not None:
            raise ValueError(f"Observation sensor with id {dto.id} already exists")

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
        if session.get(Generation, dto.generation_id) is None:
            raise ValueError(f"Generation {dto.generation_id} does not exist")

        tpms_sensors = (
            session.query(TPMSSensor)
            .filter(TPMSSensor.id.in_(dto.tpms_sensor_ids))
            .all()
        )

        missing_ids = set(dto.tpms_sensor_ids) - {sensor.id for sensor in tpms_sensors}
        if missing_ids:
            raise ValueError(f"TPMS sensors {missing_ids} do not exist")

        conflicting_car = (
            session.query(Car)
            .filter(
                Car.generation_id == dto.generation_id,
                Car.tpms_sensors.any(TPMSSensor.id.in_(dto.tpms_sensor_ids)),
            )
            .first()
        )

        if conflicting_car is not None:
            conflicting_ids = {s.id for s in conflicting_car.tpms_sensors} & set(
                dto.tpms_sensor_ids
            )
            raise ValueError(
                f"Car {conflicting_car.id} in generation {dto.generation_id} has already claimed TPMS sensors {conflicting_ids}"
            )

        car = Car.from_dto(dto, tpms_sensors)
        session.add(car)
        session.commit()
        return car.id
