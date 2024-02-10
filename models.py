from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy import Table, Column, String, Integer, MetaData

# from sqlalchemy.orm import declarative_base
# Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)


# Assuming you define your SQLAlchemy table in a separate file, e.g., models.py
# models.py
metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("username", String, unique=True, index=True),
    Column("hashed_password", String),
)

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    # car_id = Column(String, index=True)
    brand = Column(String)
    model = Column(String)
    model_year = Column(String)
    mileage = Column(String)
    fuel_type = Column(String)
    engine = Column(String)
    transmission = Column(String)

