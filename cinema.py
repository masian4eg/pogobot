import json
from dataclasses import dataclass
from datetime import datetime

import requests


@dataclass(slots=True, frozen=True)
class Film:
    title: str
    description: str
    full_description: str
    genres: str
    running_time: int
    age_restriction: str
    stars: str
    director: str
    poster: str


def get_films() -> dict:
    curr_dt = datetime.now()
    timestamp = int(round(curr_dt.timestamp()))
    url = f'https://kudago.com/public-api/v1.4/movies/?&text_format=text&location=nsk&actual_since={timestamp}'
    result = requests.get(url)
    cinema_data = result.json()

    films = {}
    n = 0
    for item in cinema_data['results']:
        n += 1
        films[n] = [item['title'], item['id']]
    return films


def get_film_data(id: int) -> json:
    url = f'https://kudago.com/public-api/v1.4/movies/{id}/' \
          f'?fields=title,description,body_text,genres,running_time,age_restriction,stars,director,poster'
    result = requests.get(url)
    film_data = result.json()
    return film_data


def _parse_film_attributes(id: int) -> Film:
    film = get_film_data(id)
    return Film(
        title=film['title'],
        description=film['description'],
        full_description=film['body_text'],
        genres=film['genres'][0]['name'],
        running_time=film['running_time'],
        age_restriction=film['age_restriction'],
        stars=film['stars'],
        director=film['director'],
        poster=film['poster']['image'],
    )


def num_to_id(num: str) -> int:
    num = int(num)
    films_dict = get_films()
    film_id = films_dict[num][1]
    return film_id


def get_film(id: int) -> Film:
    film = _parse_film_attributes(id)
    return film
