from enum import Enum
from typing import NamedTuple
import json
from json.decoder import JSONDecodeError
import ssl
import urllib.request
from urllib.error import URLError
import asyncio

from coordinates import Coordinates, getlocation
import config
from exceptions import ApiServiceError


Celsius = int
type_weather = str
speed = int


class Weather(NamedTuple):
    temperature: Celsius
    weather_type: type_weather
    city: str
    wind: speed


def get_weather(coordinates: Coordinates):
    '''Принимает координаты из Gismeteo API и возвращает погоду'''
    gismeteo_response = _get_gismeteo_response(
        longitude=coordinates.longitude, latitude=coordinates.latitude)
    weather = _parse_gismeteo_response(gismeteo_response)
    return weather


def _get_gismeteo_response(latitude: float, longitude: float) -> str:
    ssl._create_default_https_context = ssl._create_unverified_context
    url = config.GISMETEO_URL.format(
        latitude=latitude, longitude=longitude)
    try:
        response = urllib.request.urlopen(url)
        gismeteo_response = response.read()
        return gismeteo_response
    except URLError as e:
        print(f"Ошибка запроса: {e.reason}")
        raise ApiServiceError


def _parse_gismeteo_response(gismeteo_response: str) -> Weather:
    try:
        gismeteo_dict = json.loads(gismeteo_response)
    except JSONDecodeError:
        print('Невозможно считать файл JSON')
        raise ApiServiceError
    return Weather(
        temperature=_parse_temperature(gismeteo_dict),
        weather_type=_parse_weather_type(gismeteo_dict),
        city=getlocation,
        wind=_parse_wind(gismeteo_dict)
    )


def _parse_temperature(gismeteo_dict: dict) -> Celsius:
    return round(gismeteo_dict["response"]["temperature"]["air"]["C"])


def _parse_weather_type(gismeteo_dict: dict) -> type_weather:
    try:
        return gismeteo_dict["response"]["description"]["full"]
    except KeyError:
        print('Ошибка ключа')
        raise ApiServiceError


def _parse_wind(gismeteo_dict: dict) -> speed:
    return gismeteo_dict["response"]["wind"]["speed"]["m_s"]


if __name__ == "__main__":
    print(get_weather(Coordinates(latitude=55.7, longitude=37.6)))
    weather = asyncio.run(get_weather(Coordinates))