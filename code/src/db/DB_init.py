from sqlalchemy import create_engine, event, inspect
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from config import DB_URL

engine = create_engine(DB_URL)
DBSession = sessionmaker(bind=engine)
inspector = inspect(engine)


@event.listens_for(engine, "connect")
def enable_foreign_keys(connection, _):
    connection.execute("PRAGMA foreign_keys=ON")


class Base(DeclarativeBase):
    pass
