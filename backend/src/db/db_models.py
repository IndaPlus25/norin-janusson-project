from datetime import datetime, timezone
from sqlalchemy import JSON, DateTime, ForeignKey
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from data.enums import EPSG
from data.DTO_objects import (
    CarObservationResponseDto,
    CarResponseDto,
    CreateCarDto,
    CreateCarObservationDto,
    CreateGenerationDto,
    CreateObservationSensorDto,
    CreateObservationDto,
    CreateTPMSSensorDto,
    GenerationResponseDto,
    ObservationResponseDto,
    ObservationSensorResponseDto,
    TPMSSensorResponseDto,
)

from db.DB_init import Base
from data.association_tables import (
    car_observation_association,
    car_sensor_association,
)


class ObservationSensor(Base):
    __tablename__ = "observation_sensors"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    lat: Mapped[float] = mapped_column(nullable=False)
    lng: Mapped[float] = mapped_column(nullable=False)
    epsg: Mapped[EPSG] = mapped_column(SQLAlchemyEnum(EPSG), nullable=False)
    address: Mapped[str] = mapped_column(nullable=False)
    active: Mapped[bool] = mapped_column(nullable=False)
    observations: Mapped[list["Observation"]] = relationship(
        back_populates="observation_sensor", cascade="all, delete-orphan"
    )
    car_observations: Mapped[list["CarObservation"]] = relationship(
        back_populates="observation_sensor", cascade="all, delete-orphan"
    )

    @classmethod
    def from_dto(cls, dto: CreateObservationSensorDto) -> "ObservationSensor":
        return cls(
            id=dto.id,
            name=dto.name,
            lat=dto.lat,
            lng=dto.lng,
            epsg=dto.epsg,
            address=dto.address,
            active=True,
        )

    def to_dto(self) -> ObservationSensorResponseDto:
        return ObservationSensorResponseDto(
            self.id,
            self.name,
            self.lat,
            self.lng,
            self.epsg,
            self.address,
            self.active,
            [observation.id for observation in self.observations],
            [car_observation.id for car_observation in self.car_observations],
        )


class Observation(Base):
    __tablename__ = "observations"

    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    observation_sensor_id: Mapped[str] = mapped_column(
        ForeignKey("observation_sensors.id")
    )
    observation_sensor: Mapped["ObservationSensor"] = relationship(
        back_populates="observations"
    )
    tpms_sensor_id: Mapped[str] = mapped_column(ForeignKey("tpms_sensors.id"))
    tpms_sensor: Mapped["TPMSSensor"] = relationship(back_populates="observations")
    car_observations: Mapped[list["CarObservation"]] = relationship(
        secondary=car_observation_association, back_populates="observations"
    )

    @classmethod
    def from_dto(cls, dto: CreateObservationDto) -> "Observation":
        return cls(
            tpms_sensor_id=dto.tpms_sensor_id,
            observation_sensor_id=dto.observation_sensor_id,
            timestamp=dto.timestamp,
        )

    def to_dto(self) -> ObservationResponseDto:
        return ObservationResponseDto(
            self.id,
            self.timestamp,
            self.observation_sensor_id,
            self.tpms_sensor_id,
            [car_observation.id for car_observation in self.car_observations],
        )


class TPMSSensor(Base):
    __tablename__ = "tpms_sensors"

    id: Mapped[str] = mapped_column(primary_key=True)
    sensor_type: Mapped[str] = mapped_column(nullable=False)
    observations: Mapped[list["Observation"]] = relationship(
        back_populates="tpms_sensor", cascade="all, delete-orphan"
    )
    cars: Mapped[list["Car"]] = relationship(
        secondary=car_sensor_association, back_populates="tpms_sensors"
    )

    @classmethod
    def from_dto(cls, dto: CreateTPMSSensorDto) -> "TPMSSensor":
        return cls(
            id=dto.id,
            sensor_type=dto.sensor_type,
        )

    def to_dto(self) -> TPMSSensorResponseDto:
        return TPMSSensorResponseDto(
            self.id,
            self.sensor_type,
            [observation.id for observation in self.observations],
            [car.id for car in self.cars],
        )


class Car(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    generation_id: Mapped[int] = mapped_column(ForeignKey("generations.id"))
    generation: Mapped["Generation"] = relationship(back_populates="cars")
    tpms_sensors: Mapped[list["TPMSSensor"]] = relationship(
        secondary=car_sensor_association, back_populates="cars"
    )
    car_observations: Mapped[list["CarObservation"]] = relationship(
        back_populates="car", cascade="all, delete-orphan"
    )

    @classmethod
    def from_dto(cls, dto: CreateCarDto, tpms_sensors: list[TPMSSensor]) -> "Car":
        return cls(
            name=dto.name, generation_id=dto.generation_id, tpms_sensors=tpms_sensors
        )

    def to_dto(self) -> CarResponseDto:
        return CarResponseDto(
            self.id,
            self.name,
            self.generation_id,
            [tpms_sensor.id for tpms_sensor in self.tpms_sensors],
            [car_observation.id for car_observation in self.car_observations],
        )


class CarObservation(Base):
    __tablename__ = "car_observations"

    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id"))
    car: Mapped["Car"] = relationship(back_populates="car_observations")
    observations: Mapped[list["Observation"]] = relationship(
        secondary=car_observation_association, back_populates="car_observations"
    )
    observation_sensor_id: Mapped[str] = mapped_column(
        ForeignKey("observation_sensors.id")
    )
    observation_sensor: Mapped["ObservationSensor"] = relationship(
        back_populates="car_observations"
    )
    path_coordinates: Mapped[list[list[float]] | None] = mapped_column(
        JSON, nullable=True
    )

    @classmethod
    def from_dto(
        cls, dto: CreateCarObservationDto, observations: list["Observation"]
    ) -> "CarObservation":
        return cls(
            timestamp=dto.timestamp,
            car_id=dto.car_id,
            observations=observations,
            observation_sensor_id=dto.observation_sensor_id,
            path_coordinates=dto.path_coordinates,
        )

    def to_dto(self) -> CarObservationResponseDto:
        return CarObservationResponseDto(
            self.id,
            self.timestamp,
            self.car_id,
            [observation.id for observation in self.observations],
            self.observation_sensor_id,
            self.path_coordinates,
        )


class Generation(Base):
    __tablename__ = "generations"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    name: Mapped[str]
    cars: Mapped[list["Car"]] = relationship(
        back_populates="generation", cascade="all, delete-orphan"
    )

    @classmethod
    def from_dto(cls, dto: CreateGenerationDto) -> "Generation":
        return cls(
            created_at=datetime.now(timezone.utc),
            name=dto.name,
        )

    def to_dto(self) -> GenerationResponseDto:
        return GenerationResponseDto(
            self.id,
            self.created_at,
            self.name,
            [car.id for car in self.cars],
        )
