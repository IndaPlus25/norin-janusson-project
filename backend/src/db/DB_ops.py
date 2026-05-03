from datetime import datetime, timedelta, timezone

from sqlalchemy import exists, inspect, select, text
from db.DB_init import DBSession, engine
from db.DB_models import (
    Car,
    CarObservation,
    Generation,
    Observation,
    ObservationSensor,
    TPMSSensor,
)
from data.DTO_objects import (
    CarObservationResponseDto,
    CarResponseDto,
    CreateCarDto,
    CreateCarObservationDto,
    CreateGenerationDto,
    CreateObservationDto,
    CreateObservationSensorDto,
    CreateTPMSSensorDto,
    GenerationResponseDto,
    ObservationResponseDto,
    ObservationSensorResponseDto,
    TPMSSensorResponseDto,
)


def print_db() -> None:

    with DBSession() as session:
        for table_name in inspect(engine).get_table_names():
            print(f"\n=== {table_name} ===")
            result = session.execute(text(f"SELECT * FROM {table_name}"))
            rows = result.fetchall()
            if not rows:
                print("  (empty)")
            for row in rows:
                print(" ", row)


def TPMS_sensor_exists_by_id(id: str) -> bool:
    with DBSession() as session:
        return session.get(TPMSSensor, id) is not None


def observation_sensor_exists_by_id(id: str) -> bool:
    with DBSession() as session:
        return session.get(ObservationSensor, id) is not None


def create_TPMS_sensor(dto: CreateTPMSSensorDto) -> str:
    with DBSession() as session:
        if session.get(TPMSSensor, dto.id) is not None:
            raise ValueError(f"TPMS sensor {dto.id} already exists")

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


def create_car_observation(dto: CreateCarObservationDto) -> int:
    with DBSession() as session:

        if session.get(Car, dto.car_id) is None:
            raise ValueError(f"Car {dto.tpms_sensor_id} does not exist")

        if session.get(ObservationSensor, dto.observation_sensor_id) is None:
            raise ValueError(
                f"Observation sensor {dto.observation_sensor_id} does not exist"
            )
        observations = session.scalars(
            select(Observation).where(Observation.id.in_(dto.observation_ids))
        ).all()

        missing_ids = set(dto.observation_ids) - {
            observation.id for observation in observations
        }
        if missing_ids:
            raise ValueError(f"Observations {missing_ids} do not exist")

        tpms_sensor_ids: set[str] = {
            observation.tpms_sensor_id for observation in observations
        }
        tpms_sensors = session.scalars(
            select(TPMSSensor).where(
                TPMSSensor.id.in_(tpms_sensor_ids),
                TPMSSensor.cars.any(Car.id == dto.car_id),
            )
        ).all()
        missing = set(tpms_sensor_ids) - {sensor.id for sensor in tpms_sensors}

        if missing:
            raise ValueError(f"Car {dto.car_id} is not assigned sensors {missing}")

        car_observation = CarObservation.from_dto(dto, list(observations))
        session.add(car_observation)
        session.commit()
        return car_observation.id


def create_observation_sensor(dto: CreateObservationSensorDto) -> str:
    with DBSession() as session:
        if session.get(ObservationSensor, dto.id) is not None:
            raise ValueError(f"Observation sensor {dto.id} already exists")

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

        tpms_sensors = session.scalars(
            select(TPMSSensor).where(TPMSSensor.id.in_(dto.tpms_sensor_ids))
        ).all()

        missing_ids = set(dto.tpms_sensor_ids) - {sensor.id for sensor in tpms_sensors}
        if missing_ids:
            raise ValueError(f"TPMS sensors {missing_ids} do not exist")

        conflicting_car = session.scalars(
            select(Car).where(
                Car.generation_id == dto.generation_id,
                Car.tpms_sensors.any(TPMSSensor.id.in_(dto.tpms_sensor_ids)),
            )
        ).first()

        if conflicting_car is not None:
            conflicting_ids = {s.id for s in conflicting_car.tpms_sensors} & set(
                dto.tpms_sensor_ids
            )
            raise ValueError(
                f"Car {conflicting_car.id} in generation {dto.generation_id} has already claimed TPMS sensors {conflicting_ids}"
            )

        car = Car.from_dto(dto, list(tpms_sensors))
        session.add(car)
        session.commit()
        return car.id


def populate_generation_with_car_observations(
    dtos: list[CreateCarObservationDto],
) -> list[int]:
    with DBSession() as session:
        for dto in dtos:
            if session.get(Car, dto.car_id) is None:
                raise ValueError(f"Car {dto.car_id} does not exist")

            if session.get(ObservationSensor, dto.observation_sensor_id) is None:
                raise ValueError(
                    f"Observation sensor {dto.observation_sensor_id} does not exist"
                )

        all_observation_ids: set[int] = {
            id for dto in dtos for id in dto.observation_ids
        }
        observations = session.scalars(
            select(Observation).where(Observation.id.in_(all_observation_ids))
        ).all()
        missing_ids: set[int] = all_observation_ids - {
            observation.id for observation in observations
        }
        if missing_ids:
            raise ValueError(f"Observations {missing_ids} do not exist")

        observation_map: dict[int, Observation] = {obs.id: obs for obs in observations}

        all_tpms_sensor_ids: set[str] = {
            observation_map[id].tpms_sensor_id
            for dto in dtos
            for id in dto.observation_ids
        }
        tpms_sensors = session.scalars(
            select(TPMSSensor).where(
                TPMSSensor.id.in_(all_tpms_sensor_ids),
                TPMSSensor.cars.any(Car.id.in_([dto.car_id for dto in dtos])),
            )
        ).all()
        missing: set[str] = all_tpms_sensor_ids - {sensor.id for sensor in tpms_sensors}
        if missing:
            raise ValueError(f"Cars are not assigned sensors {missing}")

        car_observations: list[CarObservation] = [
            CarObservation.from_dto(
                dto, [observation_map[id] for id in dto.observation_ids]
            )
            for dto in dtos
        ]
        session.add_all(car_observations)
        session.commit()

        return [car_observation.id for car_observation in car_observations]


def populate_generation_with_cars(dtos: list[CreateCarDto]) -> list[int]:

    with DBSession() as session:
        if len(dtos) == 0:
            return []

        generation_id = dtos[0].generation_id

        if not all(x == generation_id for x in [dto.generation_id for dto in dtos]):
            raise ValueError("Conflicting generation claims")

        if session.get(Generation, generation_id) is None:
            raise ValueError(f"Generation {generation_id} does not exist")

        already_populated = session.scalar(
            select(exists().where(Car.generation_id == generation_id))
        )
        if already_populated:
            raise ValueError(f"Generation {generation_id} is already populated")

        all_sensor_ids = [id for dto in dtos for id in dto.tpms_sensor_ids]
        if len(all_sensor_ids) != len(set(all_sensor_ids)):
            raise ValueError("Conflicting TPMS sensor assignments")

        all_sensors = session.scalars(
            select(TPMSSensor).where(TPMSSensor.id.in_(all_sensor_ids))
        ).all()
        missing_ids = set(all_sensor_ids) - {sensor.id for sensor in all_sensors}
        if missing_ids:
            raise ValueError(f"TPMS sensors {missing_ids} do not exist")

        sensor_map = {sensor.id: sensor for sensor in all_sensors}

        cars = [
            Car.from_dto(dto, [sensor_map[id] for id in dto.tpms_sensor_ids])
            for dto in dtos
        ]
        session.add_all(cars)
        session.commit()

        return [car.id for car in cars]


def append_observation_to_car_observation(
    car_observation_id: int, observation_id: int
) -> None:
    with DBSession() as session:

        car_observation = session.get(CarObservation, car_observation_id)
        if car_observation is None:
            raise ValueError(f"Car observation {car_observation_id} does not exist")

        observation = session.get(Observation, observation_id)

        if observation is None:
            raise ValueError(f"Observation {observation_id} does not exist")

        if observation.tpms_sensor_id not in {
            sensor.id for sensor in car_observation.car.tpms_sensors
        }:
            raise ValueError(
                f"Car {car_observation.car_id} is not assigned sensor {observation.tpms_sensor_id}"
            )

        car_observation.observations.append(observation)
        session.add(car_observation)
        session.commit()


def update_car_name(car_id: int, new_name: str) -> CarResponseDto:
    with DBSession() as session:
        car = session.get(Car, car_id)
        if car is None:
            raise ValueError(f"Car {car_id} does not exist")
        car.name = new_name
        session.commit()
        return car.to_dto()


def get_cars_for_tpms(tpms_id: str) -> list[CarResponseDto]:
    with DBSession() as session:
        tpms_sensor = session.get(TPMSSensor, tpms_id)
        if tpms_sensor is None:
            raise ValueError(f"TPMS sensor {tpms_id} does not exist")
        return [car.to_dto() for car in tpms_sensor.cars]


def get_cars_for_generation(generation_id: int) -> list[CarResponseDto]:
    with DBSession() as session:
        generation = session.get(Generation, generation_id)
        if generation is None:
            raise ValueError(f"Generation {generation_id} does not exist")
        return [car.to_dto() for car in generation.cars]


def get_car_observations_for_car(car_id: int) -> list[CarObservationResponseDto]:
    with DBSession() as session:
        car = session.get(Car, car_id)
        if car is None:
            raise ValueError(f"Car {car_id} does not exist")
        return [car_observation.to_dto() for car_observation in car.car_observations]


def get_observation_sensor(observation_sensor_id: str) -> ObservationSensorResponseDto:
    with DBSession() as session:
        observation_sensor = session.get(ObservationSensor, observation_sensor_id)
        if observation_sensor is None:
            raise ValueError(
                f"Observation sensor {observation_sensor_id} does not exist"
            )
        return observation_sensor.to_dto()


def get_observations_for_car_observation(
    car_observation_id: int,
) -> list[ObservationResponseDto]:
    with DBSession() as session:
        car_observation = session.get(CarObservation, car_observation_id)
        if car_observation is None:
            raise ValueError(f"Car observation {car_observation_id} does not exist")
        return [observation.to_dto() for observation in car_observation.observations]


def get_generation(
    generation_id: int,
) -> GenerationResponseDto:
    with DBSession() as session:
        generation = session.get(Generation, generation_id)
        if generation is None:
            raise ValueError(f"Generation {generation_id} does not exist")
        return generation.to_dto()


def get_all_tpms_sensors() -> list[TPMSSensorResponseDto]:
    with DBSession() as session:
        tpms_sensors = session.scalars(select(TPMSSensor)).all()
        return [tpms_sensor.to_dto() for tpms_sensor in tpms_sensors]


def get_all_observations() -> list[ObservationResponseDto]:
    with DBSession() as session:
        observations = session.scalars(select(Observation)).all()
        return [observation.to_dto() for observation in observations]


def get_all_observation_sensors() -> list[ObservationSensorResponseDto]:
    with DBSession() as session:
        observation_sensors = session.scalars(select(ObservationSensor)).all()
        return [
            observation_sensor.to_dto() for observation_sensor in observation_sensors
        ]


def get_all_generations() -> list[GenerationResponseDto]:
    with DBSession() as session:
        generations = session.scalars(select(Generation)).all()
        return [generation.to_dto() for generation in generations]


def get_car_observation(
    car_observation_id: int,
) -> GenerationResponseDto:
    with DBSession() as session:
        car_observation = session.get(CarObservation, car_observation_id)
        if car_observation is None:
            raise ValueError(f"Car observation {car_observation_id} does not exist")
        return car_observation.to_dto()


def get_recent_car_observations_for_generation(
    generation_id: int, max_age_ms: int
) -> list[CarObservationResponseDto]:
    with DBSession() as session:
        if session.get(Generation, generation_id) is None:
            raise ValueError(f"Generation {generation_id} does not exist")
        cutoff = datetime.now(timezone.utc) - timedelta(milliseconds=max_age_ms)
        car_observations = session.scalars(
            select(CarObservation)
            .join(Car, CarObservation.car_id == Car.id)
            .where(Car.generation_id == generation_id)
            .where(CarObservation.timestamp >= cutoff)
        ).all()
        return [car_observation.to_dto() for car_observation in car_observations]
