from sqlalchemy import Column, Integer, String

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import create_engine

Base = declarative_base()


class Hurriyet(Base):
    __tablename__ = "hurriyet_ankara"

    id = Column(Integer, primary_key=True, autoincrement=True)
    link = Column(String)
    price = Column(Integer)
    title = Column(String)
    ilan_no = Column(String, unique=True)
    yer = Column(String)
    oda = Column(Integer)
    metrekare = Column(Integer)
    bina_yasi = Column(Integer)
    kat = Column(Integer)
    banyo = Column(Integer)


engine = create_engine('sqlite:///parsed.db')
Base.metadata.create_all(engine)
