from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

db = []


class City(BaseModel):
    name: str
    timezone: str


@app.get("/")
def index():
    return {'key': 'value'}


@app.get("/cities")
def get_cities():
    results = []
    for city in db:
        r = requests.get(
            f"https://worldtimeapi.org/api/timezone/{city['timezone']}")
        current_timezone = r.json()['datetime']
        results.append(
            {'name': city['name'], 'timezone': city['timezone'], 'current_timezone': current_timezone})

    return results


@app.get("/cities{city_id}")
def get_city(city_id: int):
    city = db[city_id - 1]
    r = requests.get(
        f"https://worldtimeapi.org/api/timezone/{city['timezone']}")
    current_timezone = r.json()['datetime']
    return {'name': city['name'], 'timezone': city['timezone'], 'current_timezone': current_timezone}


@app.post("/cities")
def create_city(city: City):
    db.append(city.dict())
    return db[-1]


@app.delete("/cities{city_id}")
def delete_city(city_id: int):
    db.pop(city_id - 1)
    return {}
