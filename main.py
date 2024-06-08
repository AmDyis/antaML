import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from schemas import AntarktidaBase, AntarktidaList
from station import SessionLocal, Antarktida, Base, engine
import folium

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='Antarktida',
    description='Antarktida'
)

templates = Jinja2Templates(directory="templates")
#Зависимость для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, db: Session = Depends(get_db)):
    stations = db.query(Antarktida).all()
    return templates.TemplateResponse("index.html", {"request": request, "stations": stations})

@app.get("/stations", response_model=list[AntarktidaList])
def get_stations(db: Session = Depends(get_db)):
    stations = db.query(Antarktida).all()
    return stations

@app.get("/stations/{station_name}", response_model=AntarktidaBase)
def get_one_station(request: Request, station_name: str,db: Session = Depends(get_db)):
    station = db.query(Antarktida).filter(Antarktida.station_name == station_name).first()
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    return templates.TemplateResponse("station.html", {"request": request, "station": station})

@app.get("/map", response_class=HTMLResponse)
def get_map(request: Request):
    return templates.TemplateResponse("map.html", {"request": request})

@app.get("/map/{station_name}", response_class=HTMLResponse)
def get_map_station(request: Request, station_name: str, db: Session = Depends(get_db)):
    station = db.query(Antarktida).filter(Antarktida.station_name == station_name).first()

    if not station:  # Вот здесь исправление
        return "Станция не найдена"

    # Создаем объект карты Folium
    map = folium.Map(location=[station.latitude, station.longitude], zoom_start=1)

    # Добавляем маркер на карту
    folium.Marker(
        location=[station.latitude, station.longitude],
        popup=station.station_name,
        tooltip=station.station_name
    ).add_to(map)

    # Сохраняем карту в виде HTML
    map_html = map._repr_html_()

    # Возвращаем HTML-страницу с картой
    return templates.TemplateResponse("get_single_map.html", {"request": request, "station_name": station.station_name, "latitude": station.latitude, "longitude": station.longitude, "lvlsea": station.lvlsea})


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)
