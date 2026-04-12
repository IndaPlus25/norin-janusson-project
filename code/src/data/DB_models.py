from datetime import datetime
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy import Enum as SQLAlchemyEnum
from enum import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from data.DTO_objects import (
    CarResponseDto,
    CreateCarDto,
    CreateCarObservationDto,
    CreateGenerationDto,
    CreateObservationSensorDto,
    CreateObservationDto,
    CreateTPMSSensorDto,
)

from db.DB_init import Base
from data.association_tables import (
    car_observation_association,
    car_sensor_association,
)


class EPSG(int, Enum):
    STANDARD = 4326


class ObservationSensor(Base):
    __tablename__ = "observation_sensors"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    lat: Mapped[float] = mapped_column(nullable=False)
    lng: Mapped[float] = mapped_column(nullable=False)
    epsg: Mapped[EPSG] = mapped_column(SQLAlchemyEnum(EPSG), nullable=False)
    active: Mapped[bool] = mapped_column(nullable=False)
    observations: Mapped[list["Observation"]] = relationship(
        back_populates="observation_sensor", cascade="all, delete-orphan"
    )
    car_observation_association: Mapped[list["CarObservation"]] = relationship(
        back_populates="observation_sensor", cascade="all, delete-orphan"
    )

    @classmethod
    def from_dto(cls, dto: CreateObservationSensorDto) -> "ObservationSensor":
        return cls(
            id=dto.id,
            name=dto.name,
            lat=dto.lat,
            lng=dto.lng,
            epsg=EPSG.STANDARD,
            active=True,
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

    @classmethod
    def from_dto(
        cls, dto: CreateCarObservationDto, observations: list[TPMSSensor]
    ) -> "Car":
        return cls(
            timestamp=dto.timestamp,
            car_id=dto.car_id,
            observations=observations,
            observation_sensor_id=dto.observation_sensor_id,
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
            created_at=dto.created_at,
            name=dto.name,
        )
