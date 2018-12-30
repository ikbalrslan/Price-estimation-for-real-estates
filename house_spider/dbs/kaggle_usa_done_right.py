from sqlalchemy import Column, Integer, String, REAL

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import create_engine

Base = declarative_base()


class Kaggle(Base):
    __tablename__ = "HOUSE_DATA"

    ID = Column(Integer)
    UNIQUE_ID = Column(Integer, primary_key=True)
    DATE_TIME = Column(String)
    PRICE = Column(REAL)
    BEDROOMS = Column(Integer)
    BATHROOMS = Column(Integer)
    SQFT_LIVING = Column(Integer)
    SQFT_LOT = Column(Integer)
    FLOORS = Column(Integer)
    WATERFRONT = Column(Integer)
    VIEW_COUNT = Column(Integer)
    CONDITION = Column(Integer)
    GRADE = Column(Integer)
    SQFT_ABOVE = Column(Integer)
    SQFT_BASEMENT = Column(Integer)
    YR_BUILT = Column(Integer)
    YR_RENOVATED = Column(Integer)
    ZIPCODE = Column(Integer)
    LAT = Column(REAL)
    LONG = Column(REAL)
    SQFT_LIVING15 = Column(Integer)
    SQFT_LOT15 = Column(Integer)


engine = create_engine('sqlite:///usa_kaggle.db')
Base.metadata.create_all(engine)
