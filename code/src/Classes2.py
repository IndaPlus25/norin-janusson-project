from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from DBinit import Base

class Observation(Base):
    __tablename__ = "observations"

    id = Column(Integer, primary_key=True)
    tpms_sensor_id = Column(Integer, ForeignKey("tpms_sensors.id"), nullable=False)
    observation_sensor_id = Column(Integer, nullable=False)  
    timestamp = Column(DateTime, nullable=False)


class TPMSSensor(Base):
    __tablename__ = "tpms_sensors"

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    observations = relationship("Observation")