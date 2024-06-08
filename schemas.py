from pydantic import BaseModel

class AntarktidaList(BaseModel):
    station_name: str

class AntarktidaBase(BaseModel):
    id: int
    station_name: str
    year2001: float
    year2002: float
    year2003: float
    year2004: float
    year2005: float
    year2006: float
    year2007: float
    year2008: float
    year2009: float
    year2010: float
    year2011: float
    year2012: float
    year2013: float
    year2014: float
    year2015: float
    year2016: float
    year2017: float
    year2018: float
    year2019: float
    year2020: float
    year2021: float
    year2022: float
    year2023: float
    year2024: float
    year2025: float
    year2026: float
    latitude: float
    longitude: float
    lvlsea: float

    class Config:
        orm_mode = True
