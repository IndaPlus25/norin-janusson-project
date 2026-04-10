from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session

engine = create_engine("sqlite:///mydb.db")
Base = declarative_base()
