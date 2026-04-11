from datetime import datetime
from sqlalchemy import DateTime, ForeignKey
from enum import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.DB_init import Base
from data.association_tables import pruned_observation_association, car_sensor_association

# TODO: add autodeletes for empty list of references?
# TODO: add indexing for values that are frequently queried by?

class EPSG(int, Enum):
    STANDARD = 4326


class ObservationSensor(Base):
    __tablename__ = "observation_sensors"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    lat: Mapped[float] = mapped_column(nullable=False)
    lng: Mapped[float] = mapped_column(nullable=False)
    epsg: Mapped[EPSG] = mapped_column(nullable=False)
    observations: Mapped[list["Observation"]] = relationship(
        back_populates="observation_sensor", cascade="all, delete-orphan"
    )
    pruned_observations: Mapped[list["PrunedObservation"]] = relationship(
        back_populates="observation_sensor", cascade="all, delete-orphan"
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
    pruned_observations: Mapped[list["PrunedObservation"]] = relationship(
        secondary=pruned_observation_association, back_populates="observations"
    )


class TPMSSensor(Base):
    __tablename__ = "tpms_sensors"

    id: Mapped[str] = mapped_column(primary_key=True)
    sensor_type: Mapped[str] = mapped_column(nullable=False)
    observations: Mapped[list["Observation"]] = relationship(
        back_populates="tpms_sensor"
    )
    cars: Mapped[list["Car"]] = relationship(
        secondary=car_sensor_association, back_populates="tpms_sensors"
    )


class Car(Base):
    __tablename__ = "cars"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    generation_id: Mapped[str] = mapped_column(ForeignKey("generations.id"))
    generation: Mapped["Generation"] = relationship(back_populates="cars")
    tpms_sensors: Mapped[list["TPMSSensor"]] = relationship(
        secondary=car_sensor_association, back_populates="cars"
    )
    pruned_observations: Mapped[list["PrunedObservation"]] = relationship(
        back_populates="car", cascade="all, delete-orphan"
    )


class PrunedObservation(Base):
    __tablename__ = "pruned_observations"

    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    car_id: Mapped[str] = mapped_column(ForeignKey("cars.id"))
    car: Mapped["Car"] = relationship(back_populates="pruned_observations")
    observations: Mapped[list["Observation"]] = relationship(
        secondary=pruned_observation_association, back_populates="pruned_observations"
    )
    observation_sensor_id: Mapped[str] = mapped_column(
        ForeignKey("observation_sensors.id")
    )
    observation_sensor: Mapped["ObservationSensor"] = relationship(
        back_populates="pruned_observations"
    )


class Generation(Base):
    __tablename__ = "generations"

    id: Mapped[str] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    name: Mapped[str]
    cars: Mapped[list["Car"]] = relationship(
        back_populates="generation", cascade="all, delete-orphan"
    )
