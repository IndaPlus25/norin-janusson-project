from sqlalchemy import exists, text
from db.DB_init import DBSession, inspector
from data.DB_models import Observation, TPMSSensor
from data.DTO_objects import   ObservationData, TPMSSensorData


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


def create_TPMS_sensor(data: TPMSSensorData) -> str:
    with DBSession() as session:
        tpms_sensor = TPMSSensor(**data.__dict__)
        session.add(tpms_sensor)
        session.commit()
        return tpms_sensor.id


def TPMS_sensor_exists_by_id(id: str) -> bool:
    with DBSession() as session:
        return session.query(exists().where(TPMSSensor.id == id)).scalar()


def add_observation(data: ObservationData) -> int:
    with DBSession() as session:
        observation = Observation(**data.__dict__)
        session.add(observation)
        session.commit()
        return observation.id
