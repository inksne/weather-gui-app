from typing import NamedTuple
from json.decoder import JSONDecodeError
from urllib.error import URLError
from dotenv import load_dotenv
import json
import ssl
import urllib.request
import os

from coordinates import Coordinates
import config
from exceptions import ApiServiceError

load_dotenv()
TOKEN = os.environ.get("TOKEN")

Celsius = int
type_weather = str
speed = int

class Weather(NamedTuple):
    temperature: Celsius
    weather_type: type_weather
    wind: speed

def get_weather(coordinates: Coordinates):
    '''Принимает координаты из Gismeteo API и возвращает погоду'''
    gismeteo_response = _get_gismeteo_response(
        longitude=coordinates.longitude, latitude=coordinates.latitude)
    weather = _parse_gismeteo_response(gismeteo_response, coordinates)
    return weather

def _get_gismeteo_response(latitude: float, longitude: float) -> str:
    ssl._create_default_https_context = ssl._create_unverified_context
    url = config.GISMETEO_URL.format(
        latitude=latitude, longitude=longitude, TOKEN=TOKEN)
    try:
        response = urllib.request.urlopen(url)
        gismeteo_response = response.read()
        return gismeteo_response
    except URLError as e:
        print(f"Ошибка запроса: {e.reason}")
        raise ApiServiceError

def _parse_gismeteo_response(gismeteo_response: str, coordinates: Coordinates) -> Weather:
    try:
        gismeteo_dict = json.loads(gismeteo_response)
    except JSONDecodeError:
        print('Невозможно считать файл JSON')
        raise ApiServiceError
    return Weather(
        temperature=_parse_temperature(gismeteo_dict),
        weather_type=_parse_weather_type(gismeteo_dict),
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
