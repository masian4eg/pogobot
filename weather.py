import json
from dataclasses import dataclass
from enum import IntEnum

import requests

from config import KEY_WEATHER


class WindDirection(IntEnum):
    North = 0
    Northeast = 45
    East = 90
    Southeast = 135
    South = 180
    Southwest = 225
    West = 270
    Northwest = 315


wind_name = {
    'North': 'Северный',
    'Northeast': 'Северо-восточный',
    'East': 'Восточный',
    'Southeast': 'Юго-восточный',
    'South': 'Южный',
    'Southwest': 'Юго-западный',
    'West': 'Западный',
    'Northwest': 'Северо-западный',
}


def get_wind_name(name: str) -> str:
    return wind_name[name]


@dataclass(slots=True, frozen=True)
class Weather:
    city: str
    temperature: float
    temperature_feeling: float
    temperature_from: float
    temperature_to: float
    description: str
    wind_speed: float
    wind_direction: str


def get_weather(city: str) -> Weather:
    weather = _parse_openweather_response(city)
    return weather


def get_coordinates(city: str) -> tuple[float, float]:
    url = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={KEY_WEATHER}'
    result_geo = requests.get(url)
    city_atr = result_geo.json()
    lat = city_atr[0]['lat']
    lon = city_atr[0]['lon']

    return lat, lon


def get_weather_json(city: str) -> json:
    lat, lon = get_coordinates(city)
    weather_url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}' \
                  f'&lon={lon}&appid={KEY_WEATHER}&units=metric&lang=ru'
    result = requests.get(weather_url)

    return result.json()


def get_icon():
    pass


def _parse_wind_direction(data: json) -> str:
    degrees = data['wind']['deg']
    degrees = round(degrees / 45) * 45
    if degrees == 360:
        degrees = 0
    wind_name = WindDirection(degrees).name

    return get_wind_name(f'{wind_name}')


def _parse_openweather_response(city: str) -> Weather:
    weather_data = get_weather_json(city)
    weather_data_temp = weather_data['main']
    weather_data_desc = weather_data['weather'][0]['description']
    weather_data_wind = weather_data['wind']['speed']

    return Weather(
        city=city,
        temperature=round(weather_data_temp['temp'], 1),
        temperature_feeling=round(weather_data_temp['feels_like']),
        temperature_from=round(weather_data_temp['temp_min']),
        temperature_to=round(weather_data_temp['temp_max']),
        description=weather_data_desc,
        wind_speed=round(weather_data_wind),
        wind_direction=_parse_wind_direction(weather_data),
    )
