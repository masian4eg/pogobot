from weather import get_weather
from cinema import get_films, get_film


def weather(city: str = "Новосибирск") -> str:
    wthr = get_weather(city)

    return f'{wthr.city}, {wthr.description}\n' \
           f'Температура сегодня {wthr.temperature_from}...{wthr.temperature_to}°C\n' \
           f'Сейчас {wthr.temperature}°C, ощущается как {wthr.temperature_feeling}°C\n' \
           f'{wthr.wind_direction} ветер {wthr.wind_speed} м/с'


def films() -> str:
    films = get_films()
    text_message = ''
    for num in films:
        film = films[num][0]
        text_message += f'/{num}. {film}\n'

    return text_message


def film(id: int) -> str:
    film = get_film(id)

    return f'{film.title}\n\n' \
           f'В ролях: {film.stars}<a href="{film.poster}">.</a>\n' \
           f'Режиссер: {film.director}\n\n' \
           f'{(film.full_description).replace("<p>", "").replace("</p>", "")}\n\n' \
           f'Жанр: {film.genres}\n' \
           f'Длительность {film.running_time} минут\n' \
           f'Возрастные ограничения {film.age_restriction}\n\n'


def num_answer(message: str='/weqeqwe@dfdf') -> str:
    answer = ''
    for i in message[1:]:
        if i != "@":
            answer += i
        else:
            break
    return answer
