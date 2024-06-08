from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:4545@localhost/anta"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Antarktida(Base):
    __tablename__ = "antarktida"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    station_name = Column(String, index=True)
    year2001 = Column(Float)
    year2002 = Column(Float)
    year2003 = Column(Float)
    year2004 = Column(Float)
    year2005 = Column(Float)
    year2006 = Column(Float)
    year2007 = Column(Float)
    year2008 = Column(Float)
    year2009 = Column(Float)
    year2010 = Column(Float)
    year2011 = Column(Float)
    year2012 = Column(Float)
    year2013 = Column(Float)
    year2014 = Column(Float)
    year2015 = Column(Float)
    year2016 = Column(Float)
    year2017 = Column(Float)
    year2018 = Column(Float)
    year2019 = Column(Float)
    year2020 = Column(Float)
    year2021 = Column(Float)
    year2022 = Column(Float)
    year2023 = Column(Float)
    year2024 = Column(Float)
    year2025 = Column(Float)
    year2026 = Column(Float)
    latitude = Column(Float)
    longitude = Column(Float)
    lvlsea = Column(Float)


