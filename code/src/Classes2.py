from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, create_engine
import datetime as dt

engine = create_engine("sqlite:///tables.db")


class Base(DeclarativeBase):
    pass


class Observation(Base):
    __tablename__ = "observations"

    id: Mapped[int] = mapped_column(primary_key=True)
    tpms_sensor_id: Mapped[int] = mapped_column(ForeignKey("tpms_sensors.id"))
    observation_sensor_id: Mapped[int]
    timestamp: Mapped[dt.datetime]
    sensor: Mapped["TPMSSensor"] = relationship(back_populates="observations")


class TPMSSensor(Base):
    __tablename__ = "tpms_sensors"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str]
    observations: Mapped[list["Observation"]] = relationship(back_populates="sensor")


Base.metadata.create_all(engine)
